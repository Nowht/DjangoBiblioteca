# Generated by Django 5.0.6 on 2024-11-22 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_perfilusuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfilusuario',
            name='numero_membresia',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
