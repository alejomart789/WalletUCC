# Generated by Django 4.2.1 on 2023-05-04 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0005_rename_semestre_actual_estudiante_estudiante_semestre_a_pagar_estudiante_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estudiante',
            name='fecha_a_pagar_1',
        ),
        migrations.RemoveField(
            model_name='estudiante',
            name='fecha_a_pagar_2',
        ),
        migrations.RemoveField(
            model_name='estudiante',
            name='fecha_limite_a_pagar',
        ),
    ]