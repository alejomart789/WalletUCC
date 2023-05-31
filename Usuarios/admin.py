from django.contrib import admin
from Usuarios.models import Usuario, Cuenta, Financiera, Envio, Transaccion, Estudiante

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Estudiante)
admin.site.register(Cuenta)
admin.site.register(Envio)
admin.site.register(Transaccion)
admin.site.register(Financiera)


