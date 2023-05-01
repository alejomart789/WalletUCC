from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.mail import send_mail

ROL_USUARIO_CHOICES = [('Estudiante', 'Estudiante'), ('Profesor', 'Profesor'), ('Dependencia', 'Dependencia')]

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario')
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    rol = models.CharField(max_length=50, choices=ROL_USUARIO_CHOICES)
    identificacion = models.PositiveIntegerField(unique=True)
    email = models.EmailField()
    foto_perfil = models.ImageField(upload_to='Usuarios/img/Perfil', default='Usuarios/img/Perfil/default.png', blank=True)
    amigos = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def clean(self):
        if self.rol == 'Estudiante' and getattr(self, 'profesor', None):
            raise ValidationError('Un usuario no puede ser estudiante y profesor a la vez')
        if self.rol == 'Profesor' and getattr(self, 'estudiante', None):
            raise ValidationError('Un usuario no puede ser estudiante y profesor a la vez')


class Cuenta(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='cuenta')
    saldo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.usuario.user.username

    class Meta:
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"


class Dependencia(models.Model):
    ROL_DEPENDENCIA_CHOICES = [('Financiera', 'Financiera'), ('Otra', 'Otra')]
    id_dependencia = models.PositiveIntegerField(unique=True)
    nombre = models.CharField(max_length=50)
    tipo_dependencia = models.CharField(max_length=50, choices=ROL_DEPENDENCIA_CHOICES)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    usuarios = models.ManyToManyField(Usuario, related_name='dependencias', blank=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Dependencia"
        verbose_name_plural = "Dependencias"


class Estudiante(models.Model):
    SEMESTRE_CHOICES = [(1, 'Primer Semestre'), (2, 'Segundo Semestre'), (3, 'Tercer Semestre'), (4, 'Cuarto Semestre'), (5, 'Quinto Semestre'), (6, 'Sexto Semestre'), (7, 'Séptimo Semestre'), (8, 'Octavo Semestre'), (9, 'Noveno Semestre'), (10, 'Décimo Semestre')]
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='estudiante')
    semestre_actual = models.PositiveIntegerField(choices=SEMESTRE_CHOICES)
    valor_semestre = models.DecimalField(max_digits=10, decimal_places=2)
    creditos_registrados = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.usuario.nombres} {self.usuario.apellidos} - Semestre {self.semestre_actual}'

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "
