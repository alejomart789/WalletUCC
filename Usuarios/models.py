from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    identificacion = models.PositiveIntegerField(unique=True)
    email = models.EmailField()
    foto_perfil = models.ImageField(upload_to='Usuarios/img/Perfil', default='Usuarios/img/Perfil/default.png', blank=True)
    amigos = models.ManyToManyField('self', blank=True)

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
        return f"{self.usuario.nombres} {self.usuario.apellidos} - Semestre {self.semestre_a_pagar_estudiante}"

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"


class Cuenta(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='cuenta')
    saldo_usuario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.usuario.user.username

    class Meta:
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"


class Financiera(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    saldo_financiera = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ultima_actualizacion_financiera = models.DateTimeField(auto_now=True)

    # Fechas limites de pago
    fecha_limite_pago_1 = models.DateField()
    fecha_limite_pago_2 = models.DateField()
    fecha_limite_pago_3 = models.DateField()

    aumento_1 = models.BooleanField(default=False)
    aumento_2 = models.BooleanField(default=False)
    aumento_3 = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Financiera {self.usuario.username}"

    def save(self, *args, **kwargs):
        if not Financiera.objects.filter(usuario=self.usuario).exists():
            super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Financiera"
        verbose_name_plural = "Financieras"


class Transaccion(models.Model):
    ORIGEN_FINANCIERA = 'financiera'
    DESTINO_USUARIO = 'usuario'
    ORIGEN_CHOICES = [
        (ORIGEN_FINANCIERA, 'Financiera'),
        (DESTINO_USUARIO, 'Usuario'),
    ]

    origen = models.CharField(max_length=10, choices=ORIGEN_CHOICES, default=ORIGEN_FINANCIERA)
    financiera = models.ForeignKey(
        Financiera,
        on_delete=models.CASCADE,
        related_name='transacciones_enviadas',
        null=True,
        blank=True
    )
    destino = models.ForeignKey(
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
        return f'Transacción {self.id} de {self.origen} a {self.destino}'

    def save(self, *args, **kwargs):
        if self.origen == Transaccion.ORIGEN_FINANCIERA:
            # Verificar si el origen es la financiera
            financiera = Financiera.objects.first()

            if self.destino == financiera.usuario:
                raise ValidationError('No se puede enviar una transacción a la financiera')

            financiera.saldo_financiera += self.monto_transaccion
            financiera.save()
            self.pagada_transaccion = True
        else:
            # Verificar si el origen es un usuario
            if not isinstance(self.destino, Usuario):
                raise ValidationError('El destino debe ser un usuario')

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'
        ordering = ['-fecha_transaccion']


class Envio(models.Model):
    id_envio = models.PositiveIntegerField(unique=True)
    origen_cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='envios_realizados')
    destino_cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='envios_recibidos')
    fecha_envio = models.DateTimeField(auto_now_add=True)
    monto_envio = models.DecimalField(max_digits=10, decimal_places=2)
    estado_envio = models.BooleanField(default=False)

    def __str__(self):
        return f'Envío {self.id_envio} de {self.origen_cuenta.usuario.nombres} {self.origen_cuenta.usuario.apellidos} a {self.destino_cuenta.usuario.nombres} {self.destino_cuenta.usuario.apellidos}'

    class Meta:
        verbose_name = "Envío"
        verbose_name_plural = "Envíos"

    def clean(self):
        if self.origen_cuenta.saldo_usuario < self.monto_envio:
            raise ValidationError('El usuario no tiene suficiente saldo para realizar este envío')

    def save(self, *args, **kwargs):
        if not self.pk:
            # Verificar que el usuario tenga suficiente saldo para realizar el envío
            if self.origen_cuenta.saldo_usuario < self.monto_envio:
                raise ValidationError('El usuario no tiene suficiente saldo para realizar este envío')
            # Restar el monto de la cuenta del origen
            self.origen_cuenta.saldo_usuario -= self.monto_envio
            self.origen_cuenta.save()
            # Añadir el monto a la cuenta del destino
            self.destino_cuenta.saldo_usuario += self.monto_envio
            self.destino_cuenta.save()
        super().save(*args, **kwargs)
