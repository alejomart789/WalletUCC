from django.urls import path
import Usuarios.views

urlpatterns = [
    path('login/', Usuarios.views.login, name='login'),
]