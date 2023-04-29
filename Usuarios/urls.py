from django.urls import path, include, reverse_lazy
import Usuarios.views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', Usuarios.views.login_user, name='login_user'),
    path('consola_estudiantes/', Usuarios.views.consola_estudiantes, name='consola_estudiantes'),
    
    path('mainApp/', include('mainApp.urls', namespace='main_app')),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('main_app:inicio')), name='logout'),
]