from django.db import models
from django.contrib.auth.models import User

class libros(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    genero = models.CharField(max_length=100)
    fecha_publicacion = models.DateField()
    disponibilidad = models.BooleanField(default=True)
    isbn = models.CharField(max_length=13, unique=True)
    cantidad_total = models.PositiveIntegerField(default=1)  # Cantidad total del libro en inventario
    cantidad_disponible = models.PositiveIntegerField(default=1)  # Cantidad disponible para préstamo

class Prestamo(models.Model):
    libro = models.ForeignKey(libros, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField(null=True, blank=True)
    devuelto = models.BooleanField(default=False)  # Indica si el libro ha sido devuelto

    def __str__(self):
        return f'{self.libro.titulo} - {self.usuario.username}'

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    numero_membresia = models.CharField(max_length=20, default='M')
    fecha_registro = models.DateField(auto_now_add=True)
    estado_membresia = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.numero_membresia = f"M-{self.usuario.id:05}"
        super().save(*args, **kwargs)