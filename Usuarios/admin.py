from django.contrib import admin
from Usuarios.models import Usuario, Cuenta, Dependencia, Envio, Transaccion, Estudiante

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Estudiante)
admin.site.register(Cuenta)
admin.site.register(Envio)
admin.site.register(Transaccion)

@admin.register(Dependencia)
class DependenciaAdmin(admin.ModelAdmin):
    list_display = ('id_dependencia', 'nombre_dependencia', 'tipo_dependencia', 'saldo_dependencia', 'ultima_actualizacion_dependencia')
    list_filter = ('tipo_dependencia',)
    search_fields = ('nombre_dependencia',)

