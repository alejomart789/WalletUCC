from django.contrib import admin
from Usuarios.models import Usuario, Cuenta, Dependencia, Envio, Transaccion

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Cuenta)
admin.site.register(Envio)
admin.site.register(Transaccion)

@admin.register(Dependencia)
class DependenciaAdmin(admin.ModelAdmin):
    list_display = ('id_dependencia', 'nombre', 'tipo_dependencia', 'saldo', 'ultima_actualizacion')
    list_filter = ('tipo_dependencia',)
    search_fields = ('nombre',)

