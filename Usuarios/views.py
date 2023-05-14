import decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from Usuarios.models import Financiera
from datetime import date, datetime




import locale

# Configuración para localizar el formato de números en español (Colombia)
locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')

aumentos_aplicados = set()

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
    fecha_actual = date.today()

    usuario = request.user.usuario  # se invoca al usuario que está en línea

    # Fechas límites de pago que el estudiante tiene para pagar el semestre
    financieras = Financiera.objects.all()
    primera_financiera = financieras.first()

    fechas_limites_pago = [primera_financiera.fecha_limite_pago_1, primera_financiera.fecha_limite_pago_2, primera_financiera.fecha_limite_pago_3]


    # Verificar si el aumento ya se ha aplicado para cada fecha límite
    if fecha_actual >= fechas_limites_pago[0] and fechas_limites_pago[0] not in aumentos_aplicados:
        # Aplicar el aumento correspondiente (2%)
        usuario.estudiante.valor_semestre_estudiante *= decimal.Decimal('1.02')
        aumentos_aplicados.add(fechas_limites_pago[0])

    if fecha_actual >= fechas_limites_pago[1] and fechas_limites_pago[1] not in aumentos_aplicados:
        # Aplicar el aumento correspondiente (5%)
        usuario.estudiante.valor_semestre_estudiante *= decimal.Decimal('1.05')
        aumentos_aplicados.add(fechas_limites_pago[1])

    if fecha_actual >= fechas_limites_pago[2] and fechas_limites_pago[2] not in aumentos_aplicados:
        # Aplicar el aumento correspondiente (10%)
        usuario.estudiante.valor_semestre_estudiante *= decimal.Decimal('1.10')
        aumentos_aplicados.add(fechas_limites_pago[2])

    # Guardar los cambios en el modelo Estudiante
    usuario.estudiante.save()

    # Se traen los datos del usuario
    nombre_completo = f"{usuario.nombres} {usuario.apellidos}"
    saldo = usuario.cuenta.saldo_usuario
    saldo_str = f"{saldo:,}"
    semestre_pagar = usuario.estudiante.semestre_a_pagar_estudiante
    valor_semestre_str = f"{usuario.estudiante.valor_semestre_estudiante:,}"

    return render(request, 'Estudiantes/consola_estudiantes.html', {
        'nombre_completo': nombre_completo,
        'saldo_str': saldo_str,
        'semestre_pagar': semestre_pagar,
        'valor_semestre_str': valor_semestre_str,
        'fechas_limites_pago': fechas_limites_pago,
        'fecha_actual': fecha_actual,
    })
