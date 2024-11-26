#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.contrib.auth.models import User

def create_superuser():
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL')

    if username and password and email:
        if not User.objects.filter(username=username).exists():
            print(f"Creando SuperUsuario:{username}")
            User.objects.create_superuser(username=username, password=password, email=email)
        else:
            print("SuperUsuario ya existe D:")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sitio.settings')
    try:
        from django.core.management import execute_from_command_line
        import django
        django.setup()
        create_superuser()
    except Exception as exc:
        print(f"Error Creando el SuperUsuario:{exc}")
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
