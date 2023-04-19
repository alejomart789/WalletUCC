from django.db import models

# Create your models here.
class Usuarios(models.Model):
    nombres = models.CharField(max_length=48)
    apellidos = models.CharField(max_length=48)
    identificacion = models.IntegerField()
    celular = models.BigIntegerField()
    tipo_usuario = models.CharField(max_length=48)
    correo = models.EmailField()
    contraseña = models.CharField(max_length=100)
    saldo = models.IntegerField()

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos} - CC. {self.identificacion}"       