from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib import messages
import uuid

from django.db import IntegrityError

from django.db.models import Count
from django.http import JsonResponse

from .models import *

def home(request):
    return render(request, 'landingPage/home.html')

def admin_dashboard(request):
    return render(request, 'admins/dashboardAdmin.html')

def usuario_dashboard(request):
    return render(request, 'usuarios/dashboardComun.html')

def signin(request):
    if request.method == 'GET':
        return render(request, 'login/signin.html')
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login/signin.html', {"error": "usuario o contraseña incorrectas."})

        login(request, user)
        return redirect('dashboard')

#Filtra los a los usuarios
@login_required
def dashboard(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    else:
        return redirect('usuario_dashboard')

@login_required
def signout(request):
    logout(request)
    return redirect('home')
################################################################################################

#Perfil de usuario
@login_required
def profile(request):
    perfil = request.user.perfil
    return render(request, 'usuarios/perfil.html', {'perfil':perfil})

#lista de libros que se muestran para el usuario
@login_required
def lista_libros(request):
    libros_disponibles = libros.objects.filter(cantidad_disponible__gt = 0, disponibilidad = True)
    return render(request, 'usuarios/listalibros.html', {'libro':libros_disponibles})

#lista de libros prestados por el usuario
@login_required
def lista_libros_prestados(request):
    libros_prestados = Prestamo.objects.filter(usuario=request.user)
    libros = [prestado.libro for prestado in libros_prestados]
    return render(request, 'usuarios/librosprestados.html', {'libro':libros})

#usuario solicitanddo libros
@login_required
def solicitar_libro(request,id):
    libro = libros.objects.get(id=id)
    
    if libro.cantidad_disponible > 0:
        # Crear un préstamo para el usuario
        prestamo = Prestamo.objects.create(libro=libro, usuario=request.user)
        
        # Decrementar la cantidad disponible del libro
        libro.cantidad_disponible -= 1
        libro.save()
        
        return redirect('lista_libros')  # Redirigir a la lista de libros disponibles
    else:
        # Si no hay libros disponibles
        return render(request, 'sin_disponibilidad.html', {'libro': libro})
    
################################################################################################
    
######################################################################################    
# Verificar si el usuario es administrador
def es_admin(user):
    return user.is_staff

#Lista de usuarios
@user_passes_test(es_admin)
def lista_usuario(request):
    usuarios = User.objects.select_related("perfil").all()
    return render(request, 'admins/Perfil_usuarios.html', {'usuarios':usuarios})

#Nuevo Usuario
@user_passes_test(es_admin)
def nuevo_usuario(request):
    if request.method == 'POST':
        datos = request.POST.dict()

        if User.objects.filter(username=datos['username']).exists():
            return render(request, 'admins/registro.html', {'error':'El nombre de usuario ya existe'})

        if User.objects.filter(email=datos['email']).exists():
            return render(request, 'admins/registro.html', {'error':'El correo electronico ya existe'})

        new_usuario = User.objects.create_user(
            username=datos['username'],
            password=datos['password'],
            email=datos['email'],
        )

        if 'es_admin' in datos :
            new_usuario.is_staff = True
        new_usuario.save()

        return redirect('usuarios')

    return render(request, 'admins/registro.html')

#Eliminar Usuarios
@user_passes_test(es_admin)
def eliminar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    if request.user.is_staff: 
        usuario.delete()
        return redirect('usuarios')
    
#Actualizar usuarios
@user_passes_test(es_admin)
def actualizar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    profile = get_object_or_404(PerfilUsuario, usuario=usuario)
    datos = request.POST
    usuario.username = datos.get('username', usuario.username)
    usuario.email = datos.get('email', usuario.email)
    profile.estado_membresia = datos.get('estado_membresia', profile.estado_membresia)
    if datos.get('password'):  # Si se proporciona una nueva contraseña
        usuario.set_password(datos['password'])
    usuario.save()
    profile.save()
    return redirect('usuarios') 

# Vista para los administradores gestionar inventario
@user_passes_test(es_admin)
def gestionar_inventario(request):
    lista = libros.objects.all()
    return render(request, 'admins/gestionar_inventario.html', {'libros': lista})

#Vista para agregar libros
@user_passes_test(es_admin)
def agregar_libros(request):
    gender = genero.objects.all()
    if request.method == 'POST':
        nuevo_libro = request.POST.dict()
        libro_genero = genero.objects.get(id=nuevo_libro['genero'])

        try:
            new_book, nuevo = libros.objects.get_or_create(
            titulo = nuevo_libro['titulo'],
            autor = nuevo_libro['autor'],
            genero = libro_genero,
            fecha_publicacion = nuevo_libro['fecha_publicacion'],
            disponibilidad = nuevo_libro['disponibilidad'],
            isbn = nuevo_libro['isbn'],
            cantidad_total = nuevo_libro['cantidad_total'],
            cantidad_disponible = nuevo_libro['cantidad_disponible'],
            
        )
            return redirect('agregar')

        except IntegrityError:
            error_isbn = f"El ISBN '{nuevo_libro['isbn']}' ya esta registrado"
            return render(request, 'admins/AgregarLibro.html',{"error":error_isbn, "genero":gender})
        
    return render(request, 'admins/AgregarLibro.html', {"genero":gender})

#Vista para agregar generos
@user_passes_test(es_admin)
def agregar_genero(request):
    nuevo = genero.objects.get_or_create(genero=request.POST['genero'])
    return redirect('agregar')

# Vista para actualizar datos de los libros
@user_passes_test(es_admin)
def actualizar_libros(request, id):
    book = libros.objects.get(id=id)
    for key, value in request.POST.items():
            if hasattr(book, key):
                setattr(book, key, value)
    book.save()
    messages.success(request, "El libro ha sido actualizado exitosamente.")
    return redirect('inventario') 

#Vista para eliminar
@user_passes_test(es_admin)
def eliminar_libro(request, id):
    libros.objects.get(id=id).delete()
    return redirect('inventario')

# Vista para administrar préstamos y devoluciones
@user_passes_test(es_admin)
def gestionar_prestamos(request):
    prestamos = Prestamo.objects.filter(devuelto=False)
    return render(request, 'admins/gestionar_prestamos.html', {'prestamos': prestamos})

# Vista para devolver libros
@user_passes_test(es_admin)
def devolver_libro(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    libro = prestamo.libro
    
    # Marcar el préstamo como devuelto
    prestamo.devuelto = True
    prestamo.fecha_devolucion = timezone.now()
    prestamo.save()
    
    # Aumentar la cantidad disponible del libro
    libro.cantidad_disponible += 1
    libro.save()
    
    return redirect('prestamos')  # Redirige a la página de gestionar préstamos

#Vista para el historial de prestamos
@user_passes_test(es_admin)
def historial_devoluciones(request):
    devoluciones = Prestamo.objects.filter(devuelto=True)
    return render(request, "admins/historial_devoluciones.html",{'devoluciones':devoluciones})
#################################################################################################

#calculo de libros 
def libros_mas_prestados(request):
    # Agrupar por libro y contar préstamos
    prestamos = (
        Prestamo.objects.values('libro__titulo')
        .annotate(total_prestamos=Count('libro'))
        .order_by('-total_prestamos')[:5]  # Mostrar solo los 5 más prestados
    )

    # Preparar los datos para JSON
    data = {
        "labels": [item['libro__titulo'] for item in prestamos],
        "values": [item['total_prestamos'] for item in prestamos],
    }
    return JsonResponse(data)