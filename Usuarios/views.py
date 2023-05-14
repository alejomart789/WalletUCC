import decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from Usuarios.models import Financiera
from datetime import datetime




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

# Lo que se llama cada vez que se recarga la consola estudiantes
@login_required
def consola_estudiantes(request):
    fecha_actual = datetime.now()

    usuario = request.user.usuario # se invoca al usuario que esta en linea

    # Se traen los datos del usuario
    nombre_completo = f"{usuario.nombres} {usuario.apellidos}"
    saldo = usuario.cuenta.saldo_usuario
    saldo_str = f"{saldo:,}"
    semestre_pagar = usuario.estudiante.semestre_a_pagar_estudiante
    valor_semestre_str = f"{usuario.estudiante.valor_semestre_estudiante:,}"

    # Fechas limites de pago que el estudiante tiene para pagar el semestre
    financieras = Financiera.objects.all()
    primera_financiera = financieras.first()

    fechas_limites_pago = [primera_financiera.fecha_limite_pago_1, primera_financiera.fecha_limite_pago_2, primera_financiera.fecha_limite_pago_3]

    return render(request, 'Estudiantes/consola_estudiantes.html', {
        'nombre_completo': nombre_completo,
        'saldo_str': saldo_str,
        'semestre_pagar': semestre_pagar,
        'valor_semestre_str': valor_semestre_str,
        'fechas_limites_pago': fechas_limites_pago,
        'fecha_actual': fecha_actual,
    })


@login_required
def aumento_semestre(request):


    return redirect('consola_estudiantes')