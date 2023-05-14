import decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from datetime import date, datetime


import locale

# Configuración para localizar el formato de números en español (Colombia)
locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')

# Auntificacion de usuario
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
    usuario = request.user.usuario

    nombre_completo = f"{usuario.nombres_usuario} {usuario.apellidos_usuario}"

    fechas_limite = get_fechas_limite()

    foto_perfil_url = usuario.foto_perfil_usuario.url

    saldo = usuario.cuenta.saldo_usuario
    saldo_str = f"{saldo:,}"
    semestre_pagar = usuario.estudiante.semestre_a_pagar_estudiante
    valor_semestre_str = f"{usuario.estudiante.valor_semestre_estudiante:,}"

    return render(request, 'Estudiantes/consola_estudiantes.html', {
        'nombre_completo': nombre_completo,
        'foto_perfil': foto_perfil_url,
        'saldo_str': saldo_str,
        'semestre_pagar': semestre_pagar,
        'valor_semestre_str': valor_semestre_str,
        'fechas_limite': fechas_limite,
    })


@login_required
def aumento_semestre(request):
    usuario = request.user.usuario

    fecha_actual = datetime.now().date()

    fechas_limite = get_fechas_limite()

    valor_semestre = usuario.estudiante.valor_semestre_estudiante

    for fecha in fechas_limite:
        if fecha_actual > fecha:  # Corregir la condición aquí
            if fecha >= fechas_limite[0] and fecha <= fechas_limite[1]:
                valor_semestre *= decimal.Decimal('1.05')
            elif fecha > fechas_limite[1] and fecha <= fechas_limite[2]:
                valor_semestre *= decimal.Decimal('1.1')
            elif fecha > fechas_limite[2]:
                valor_semestre *= decimal.Decimal('1.15')

    usuario.estudiante.valor_semestre_estudiante = valor_semestre
    usuario.estudiante.save()

    return redirect('consola_estudiantes')

def get_fechas_limite():
    return [
        date(2023, 5, 7),
        date(2023, 7, 28),
        date(2023, 8, 4),
    ]
