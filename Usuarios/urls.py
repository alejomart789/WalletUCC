from django.urls import path, include, reverse_lazy
import Usuarios.views
from django.contrib.auth.views import LogoutView

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views



urlpatterns = [
    path('login/', Usuarios.views.login_user, name='login_user'),
    path('consola_estudiantes/', Usuarios.views.consola_estudiantes, name='consola_estudiantes'),
    path('realizar-pago-semestre/', views.realizar_pago_semestre, name='realizar_pago_semestre'),
    path('actualizar_perfil/', views.actualizar_perfil, name='actualizar_perfil'),
    
    path('consola_financiera/', Usuarios.views.consola_financiera, name='consola_financiera'),
    path('perfil_estudiante/', Usuarios.views.perfil_estudiante, name="perfil_estudiante"),
    path('financiera/perfil_financiera/', Usuarios.views.perfil_financiera, name="perfil_financiera"),
    path('actualizar_perfil_financiera/', views.actualizar_perfil_financiera, name='actualizar_perfil_financiera'),
    path('transacciones_financiera/', views.transacciones_financiera, name='transacciones_financiera'),
    
    path('mainApp/', include('mainApp.urls', namespace='main_app')),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('main_app:inicio')), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)