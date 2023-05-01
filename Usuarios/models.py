from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
<<<<<<< HEAD
from django.core.mail import send_mail
=======
>>>>>>> e63b12f (Se realizar la base de datos inicial con todos los requerimientos del proyecto)

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
<<<<<<< HEAD
        if self.rol == 'Estudiante' and getattr(self, 'profesor', None):
            raise ValidationError('Un usuario no puede ser estudiante y profesor a la vez')
        if self.rol == 'Profesor' and getattr(self, 'estudiante', None):
=======
        if self.rol == 'Estudiante' and hasattr(self, 'profesor'):
            raise ValidationError('Un usuario no puede ser estudiante y profesor a la vez')
        if self.rol == 'Profesor' and hasattr(self, 'estudiante'):
>>>>>>> e63b12f (Se realizar la base de datos inicial con todos los requerimientos del proyecto)
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


<<<<<<< HEAD
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
=======
class Envio(models.Model):
    id_envio = models.PositiveIntegerField(unique=True)
    origen = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='envios_realizados')
    destino = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='envios_recibidos')
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.BooleanField(default=False)

    def __str__(self):
        return f'Envío {self.id_envio} de {self.origen.usuario.nombres} {self.origen.usuario.apellidos} a {self.destino.usuario.nombres} {self.destino.usuario.apellidos}'

    class Meta:
        verbose_name = "Envío"
        verbose_name_plural = "Envíos"


class Transaccion(models.Model):
    dependencia = models.ForeignKey(Dependencia, on_delete=models.CASCADE, related_name='transacciones')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='transacciones')
    info_factura = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateTimeField(null=True, blank=True)
    pagada = models.BooleanField(default=False)

    def __str__(self):
        return f'Transacción {self.id} de {self.usuario.user.username} a {self.dependencia.nombre}'

    class Meta:
        verbose_name = "Transacción"
        verbose_name_plural = "Transacciones"
        ordering = ['-fecha']

    def clean(self):
        if self.monto <= 0:
            raise ValidationError('El monto de la transacción debe ser mayor a cero')
        if self.fecha_vencimiento and self.fecha_vencimiento <= self.fecha:
            raise ValidationError('La fecha de vencimiento debe ser posterior a la fecha actual')
    
    def save(self, *args, **kwargs):
        # Verificar que el usuario tenga suficiente saldo para pagar la transacción
        if self.usuario.cuenta.saldo < self.monto:
            raise ValidationError('El usuario no tiene suficiente saldo para realizar esta transacción')
        # Restar el monto de la cuenta del usuario
        self.usuario.cuenta.saldo -= self.monto
        self.usuario.cuenta.save()
        # Añadir el monto a la cuenta de la dependencia
        self.dependencia.saldo += self.monto
        self.dependencia.save()
        super(Transaccion, self).save(*args, **kwargs)

    def actualizar_estado(self):
        if not self.pagada and self.fecha_vencimiento and self.fecha_vencimiento <= timezone.now():
            self.pagada = True
            self.save()

    def notificar_usuario(self):
        if not self.pagada and self.fecha_vencimiento and self.fecha_vencimiento <= timezone.now():
            mensaje = f'La transacción {self.id} con la dependencia {self.dependencia.nombre} está pendiente de pago'
            # Enviar notificación al usuario
            pass
>>>>>>> e63b12f (Se realizar la base de datos inicial con todos los requerimientos del proyecto)
