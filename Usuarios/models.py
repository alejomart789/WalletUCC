from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.exceptions import PermissionDenied

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario')
    nombres_usuario = models.CharField(max_length=50)
    apellidos_usuario = models.CharField(max_length=50)
    identificacion_usuario = models.PositiveIntegerField(unique=True)
    email_usuario = models.EmailField()
    foto_perfil_usuario = models.ImageField(upload_to='Usuarios/img/Perfil', default='Usuarios/img/Perfil/default.png', blank=True)
    amigos_usuario = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

class Estudiante(models.Model):
    usuario_estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    valor_semestre_estudiante = models.DecimalField(max_digits=15, decimal_places=2)
    creditos_registrados_estudiante = models.PositiveIntegerField()
    semestre_actual_estudiante = models.PositiveIntegerField()


class Cuenta(models.Model):
    usuario_cuenta = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='Cuenta')
    saldo_usuario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.usuario_cuenta.user.username

    class Meta:
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"


class Dependencia(models.Model):
    ROL_DEPENDENCIA_CHOICES = [('Financiera', 'Financiera'), ('Otra', 'Otra')]
    id_dependencia = models.PositiveIntegerField(unique=True)
    nombre_dependencia = models.CharField(max_length=50)
    tipo_dependencia = models.CharField(max_length=50, choices=ROL_DEPENDENCIA_CHOICES)
    saldo_dependencia = models.DecimalField(max_digits=10, decimal_places=2)
    usuarios_dependencia = models.ManyToManyField(Usuario, related_name='dependencias', blank=True)
    ultima_actualizacion_dependencia = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre_dependencia

    class Meta:
        verbose_name = "Dependencia"
        verbose_name_plural = "Dependencias"


class Envio(models.Model):
    id_envio = models.PositiveIntegerField(unique=True)
    origen_cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='envios_realizados')
    destino_cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='envios_recibidos')
    fecha_envio = models.DateTimeField(auto_now_add=True)
    monto_envio = models.DecimalField(max_digits=10, decimal_places=2)
    estado_envio = models.BooleanField(default=False)

    def __str__(self):
        return f'Envío {self.id_envio} de {self.origen.usuario.nombres} {self.origen.usuario.apellidos} a {self.destino.usuario.nombres} {self.destino.usuario.apellidos}'

    class Meta:
        verbose_name = "Envío"
        verbose_name_plural = "Envíos"


class Transaccion(models.Model):
    dependencia_origien = models.ForeignKey(Dependencia, on_delete=models.CASCADE, related_name='transacciones')
    usuario_destino = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='transacciones')
    info_factura_dependencia = models.CharField(max_length=100)
    monto_transaccion = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_transaccion = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento_transaccion = models.DateTimeField(null=True, blank=True)
    pagada_transaccion = models.BooleanField(default=False)

    def __str__(self):
        return f'Transacción {self.id} de {self.usuario_destino.user.username} a {self.dependencia_origien.nombre_dependencia}'

    class Meta:
        verbose_name = "Transacción"
        verbose_name_plural = "Transacciones"
        ordering = ['-fecha_transaccion']

    def clean(self):
        if self.monto <= 0:
            raise ValidationError('El monto de la transacción debe ser mayor a cero')
        if self.fecha_vencimiento_transaccion and self.fecha_vencimiento_transaccion <= self.fecha:
            raise ValidationError('La fecha de vencimiento debe ser posterior a la fecha actual')
    
    def save(self, *args, **kwargs):
        # Verificar que el usuario tenga suficiente saldo para pagar la transacción
        if self.usuario_destino.Cuenta.saldo_usuario < self.monto_transaccion:
            raise ValidationError('El usuario no tiene suficiente saldo para realizar esta transacción')
        # Restar el monto de la cuenta del usuario
        self.usuario_destino.Cuenta.saldo_usuario -= self.monto_transaccion
        self.usuario.Cuenta.save()
        # Añadir el monto a la cuenta de la dependencia
        self.dependencia_origien.saldo_dependencia += self.monto_transaccion
        self.Dependencia.save()
        super(Transaccion, self).save(*args, **kwargs)

    def actualizar_estado(self):
        if not self.pagada and self.fecha_vencimiento and self.fecha_vencimiento <= timezone.now():
            self.pagada = True
            self.save()

    def notificar_usuario(self):
        if not self.pagada_transaccion and self.fecha_vencimiento and self.fecha_vencimiento <= timezone.now():
            mensaje = f'La transacción {self.id} con la dependencia {self.dependencia.nombre} está pendiente de pago'
            # Enviar notificación al usuario
            pass
