from django.shortcuts import render

def login(request):
    # tu código de autenticación
    return render(request, 'Usuarios/login.html')
