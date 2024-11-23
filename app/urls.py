from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('signin/', signin, name='signin'),
    path('logout/', signout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('user-dashboard/', usuario_dashboard, name='usuario_dashboard'),
    path('perfil/', profile, name='perfil_usuario'),
    path('agregar/',agregar_libros,name='agregar'),
    path('inventario/',gestionar_inventario,name='inventario'),
    path('libros/',lista_libros,name='lista_libros'),
    path('solicitud/<int:id>/',solicitar_libro,name='solicitud'),
    path('prestamos/',gestionar_prestamos,name='prestamos'),
    path('actualizar/<int:id>/',actualizar_libros,name='actualizar'),
    path('eliminar/<int:id>/',eliminar_libro,name='eliminar'),
    path('devolver/<int:prestamo_id>/',devolver_libro,name='devolver'),
    path('historial-devoluciones/',historial_devoluciones,name='historiald'),
    path('usuarios/',lista_usuario,name='usuarios'),
    path('registro/',nuevo_usuario,name='registro'),
    path('delete/<int:id>/',eliminar_usuario,name='delete_user'),
    path('update/<int:id>/',actualizar_usuario,name='update_user'),

    path('libros-mas-prestados/', libros_mas_prestados, name='libros_mas_prestados'),
]