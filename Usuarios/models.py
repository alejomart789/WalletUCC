from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario')
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    tipo_usuario = models.CharField(max_length=50)
    identificacion = models.PositiveIntegerField(unique=True)
    email = models.EmailField()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

class Estudiante(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='estudiante')
    codigo_estudiante = models.PositiveIntegerField(unique=True)
    carrera = models.CharField(max_length=50)

    def __str__(self):
        return self.usuario.username

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        
class Profesor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profesor')
    codigo_profesor = models.PositiveIntegerField(unique=True)
    facultad = models.CharField(max_length=50)

    def __str__(self):
        return self.usuario.username

    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"
        
class Cuenta(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.usuario.user.username

    class Meta:
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"
