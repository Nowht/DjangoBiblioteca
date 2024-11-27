#!/usr/bin/env python
import os
import sys

def create_superuser():
    from django.contrib.auth.models import User  # Importa dentro de la función, después de configurar Django
    # Lee las variables de entorno
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL')

    # Crea el superusuario si no existe
    if username and password and email:
        if not User.objects.filter(username=username).exists():
            print(f"Creando superusuario: {username}")
            User.objects.create_superuser(username=username, password=password, email=email)
        else:
            print("El superusuario ya existe.")

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sitio.settings")  # Cambia "tu_proyecto" por el nombre correcto
    try:
        from django.core.management import execute_from_command_line
        import django
        django.setup()  # Configura Django antes de llamar a cualquier función de Django
        create_superuser()  # Llama a la función para crear el superusuario
    except Exception as exc:
        print(f"Error creando el superusuario: {exc}")
    execute_from_command_line(sys.argv)
