from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from Usuarios.models import Usuario


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
    usuario = request.user.usuario  # Obtiene el objeto de usuario

    nombre_completo = f"{usuario.nombres_usuario} {usuario.apellidos_usuario}"
    
    foto_perfil_url = usuario.foto_perfil_usuario.url

    # Mostrar saldo del estudiante
    saldo = usuario.cuenta.saldo_usuario # obtiene el saldo de la cuenta del usuario
    saldo_str = f"{saldo:,}"  # formatea saldo con separadores de miles
    
    
    # Mostrar el valor a pagar del semestre y la fecha de pago
    valor_pagar_semestre = usuario.estudiante.valor_semestre_estudiante
    valor_pagar_semestre_str = f"{valor_pagar_semestre:,}"
    
    semestre_pagar = (usuario.estudiante.semestre_a_pagar_estudiante)
    
    return render(request, 'Estudiantes/consola_estudiantes.html', {'nombre_completo': nombre_completo, 'foto_perfil': foto_perfil_url, 'saldo_str': saldo_str, 'valor_pagar_semestre_str':valor_pagar_semestre_str, 'semestre_pagar':semestre_pagar})
