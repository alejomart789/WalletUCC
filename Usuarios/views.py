from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages

import locale

# Configuración para localizar el formato de números en español (Colombia)
locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')



def login_user(request):
    if request.user.is_authenticated:
        return redirect('consola_estudiantes')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('consola_estudiantes')
        else:
            error_message = 'Usuario o contraseña inválidos'
            messages.error(request, error_message)
            return render(request, 'Usuarios/login.html')
    else:
        return render(request, 'Usuarios/login.html')
        
@login_required
def consola_estudiantes(request):
    usuario = request.user.usuario #Llama al usuario que tiene la sesion iniciada
    
    nombre_completo = f"{usuario.nombres} {usuario.apellidos}"
    
    # Mostrar saldo del estudiante
    saldo = usuario.cuenta.saldo  # obtiene el saldo de la cuenta del usuario
    saldo_str = locale.format_string("%d", saldo, grouping=True)  # formatea saldo con separadores de miles
    
    return render(request, 'Estudiantes/consola_estudiantes.html', {'nombre_completo': nombre_completo, 'saldo_str': saldo_str})