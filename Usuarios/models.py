from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    valor_semestre_estudiante = models.DecimalField(max_digits=15, decimal_places=2)
    creditos_registrados_estudiante = models.PositiveIntegerField()
    semestre_a_pagar_estudiante = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.usuario.nombres_usuario} {self.usuario.apellidos_usuario} - Semestre {self.semestre_a_pagar_estudiante}"

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"

class Cuenta(models.Model):
    usuario_cuenta = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='cuenta')
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
        return f'Envío {self.id_envio} de {self.origen_cuenta.usuario_cuenta.nombres_usuario} {self.origen_cuenta.usuario_cuenta.apellidos_usuario} a {self.destino_cuenta.usuario_cuenta.nombres_usuario} {self.destino_cuenta.usuario_cuenta.apellidos_usuario}'

    class Meta:
        verbose_name = "Envío"
        verbose_name_plural = "Envíos"

    def clean(self):
        if self.origen_cuenta.usuario_cuenta.saldo_usuario < self.monto_envio:
            raise ValidationError('El usuario no tiene suficiente saldo para realizar este envío')

    def save(self, *args, **kwargs):
        if not self.pk:
            # Verificar que el usuario tenga suficiente saldo para realizar el envío
            if self.origen_cuenta.usuario_cuenta.saldo_usuario < self.monto_envio:
                raise ValidationError('El usuario no tiene suficiente saldo para realizar este envío')
            # Restar el monto de la cuenta del origen
            self.origen_cuenta.saldo_usuario -= self.monto_envio
            self.origen_cuenta.save()
            # Añadir el monto a la cuenta del destino
            self.destino_cuenta.saldo_usuario += self.monto_envio
            self.destino_cuenta.save()
        super().save(*args, **kwargs)

class Transaccion(models.Model):
    dependencia_origen = models.ForeignKey(
        Dependencia,
        on_delete=models.CASCADE,
        related_name='transacciones_enviadas'
    )
    usuario_destino = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='transacciones_recibidas'
    )
    info_factura_dependencia = models.CharField(max_length=100)
    monto_transaccion = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_transaccion = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento_transaccion = models.DateTimeField(null=True, blank=True)
    pagada_transaccion = models.BooleanField(default=False)

    def __str__(self):
        return f'Transacción {self.id} de {self.usuario_destino.user.username} a {self.dependencia_origen.nombre_dependencia}'

    class Meta:
        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'
        ordering = ['-fecha_transaccion']

    def clean(self):
        if self.monto_transaccion <= 0:
            raise ValidationError('El monto de la transacción debe ser mayor a cero')
        if self.fecha_vencimiento_transaccion and self.fecha_vencimiento_transaccion <= timezone.now():
            raise ValidationError('La fecha de vencimiento debe ser posterior a la fecha actual')

    def save(self, *args, **kwargs):
        # Verificar que el usuario tenga suficiente saldo para pagar la transacción
        if self.usuario_destino.usuario_cuenta.saldo_usuario < self.monto_transaccion:
            raise ValidationError('El usuario no tiene suficiente saldo para realizar esta transacción')
        # Restar el monto de la cuenta del usuario
        self.usuario_destino.usuario_cuenta.saldo_usuario -= self.monto_transaccion
        self.usuario_destino.usuario_cuenta.save()
        # Añadir el monto a la cuenta de la dependencia
        self.dependencia_origen.saldo_dependencia += self.monto_transaccion
        self.dependencia_origen.save()
        super().save(*args, **kwargs)

    def actualizar_estado(self):
        if not self.pagada_transaccion and self.fecha_vencimiento_transaccion and self.fecha_vencimiento_transaccion <= timezone.now():
            self.pagada_transaccion = True
            self.save()