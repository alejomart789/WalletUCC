from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

TIPO_USUARIO_CHOICES = [    ('Estudiante', 'Estudiante'),    ('Profesor', 'Profesor'),    ('Dependencia', 'Dependencia'),]

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario')
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    tipo_usuario = models.CharField(max_length=50, choices=TIPO_USUARIO_CHOICES)
    identificacion = models.PositiveIntegerField(unique=True)
    email = models.EmailField()
    foto_perfil = models.ImageField(upload_to='Usuarios/img/Perfil', default='Usuarios/img/Perfil/default.png', blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def clean(self):
        if self.tipo_usuario == 'Estudiante' and hasattr(self, 'profesor'):
            raise ValidationError('Un usuario no puede ser estudiante y profesor a la vez')
        if self.tipo_usuario == 'Profesor' and hasattr(self, 'estudiante'):
            raise ValidationError('Un usuario no puede ser estudiante y profesor a la vez')


class Estudiante(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='estudiante')
    codigo_estudiante = models.PositiveIntegerField(unique=True)
    carrera = models.CharField(max_length=50)

    def __str__(self):
        return self.usuario.username

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"

    def clean(self):
        if Profesor.objects.filter(usuario=self.usuario).exists():
            raise ValidationError('El usuario ya tiene un perfil de profesor')
        

class Profesor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profesor')
    codigo_profesor = models.PositiveIntegerField(unique=True)
    facultad = models.CharField(max_length=50)

    def __str__(self):
        return self.usuario.username

    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"

    def clean(self):
        if Estudiante.objects.filter(usuario=self.usuario).exists():
            raise ValidationError('El usuario ya tiene un perfil de estudiante')

        
class Cuenta(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='cuenta')
    saldo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.usuario.user.username

    class Meta:
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"


class Dependencia(models.Model):
    id_dependencia = models.PositiveIntegerField(unique=True)
    nombre = models.CharField(max_length=50)
    tipo_dependencia = models.CharField(max_length=50)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    usuarios = models.ManyToManyField(Usuario, related_name='dependencias', blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Dependencia"
        verbose_name_plural = "Dependencias"


