from django.urls import path
import Usuarios.views

urlpatterns = [
    path('login/', Usuarios.views.login_user, name='login_user'),
    path('consola_estudiantes/', Usuarios.views.consola_estudiantes, name='consola_estudiantes'),
]