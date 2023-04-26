from django.contrib import admin
from Usuarios.models import Usuario, Estudiante, Profesor, Cuenta

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Estudiante)
admin.site.register(Profesor)
admin.site.register(Cuenta)