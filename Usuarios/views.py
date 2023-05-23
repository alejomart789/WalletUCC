import decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from Usuarios.models import Financiera
from datetime import date, datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from Usuarios.models import Estudiante, Cuenta


from decimal import Decimal
from django.http import HttpResponse

import locale

# Configuración para localizar el formato de números en español (Colombia)
locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')

class ObservadorSemestre:
    def __init__(self, estudiante, financiera):
        self.estudiante = estudiante
        self.financiera = financiera

    def actualizar(self, request):
        fecha_actual = date.today()
        fecha_limite_pago_1 = self.financiera.fecha_limite_pago_1
        fecha_limite_pago_2 = self.financiera.fecha_limite_pago_2
        fecha_limite_pago_3 = self.financiera.fecha_limite_pago_3

        if fecha_actual > fecha_limite_pago_1 and not self.estudiante.aumento_1:
            self.aumentar_semestre(request, 1)
        elif fecha_actual > fecha_limite_pago_2 and not self.estudiante.aumento_2:
            self.aumentar_semestre(request, 2)
        elif fecha_actual > fecha_limite_pago_3 and not self.estudiante.aumento_3:
            self.aumentar_semestre(request, 3)

    def aumentar_semestre(self, request, aumento):
        if aumento == 1:
            incremento = Decimal('0.02')
            self.estudiante.valor_semestre_estudiante += self.estudiante.valor_semestre_estudiante * incremento
            self.estudiante.aumento_1 = True
            mensaje = "¡Se ha aplicado el primer aumento al semestre!"
        elif aumento == 2:
            incremento = Decimal('0.05')
            self.estudiante.semestre_a_pagar_estudiante += self.estudiante.valor_semestre_estudiante * incremento
            self.estudiante.aumento_2 = True
            mensaje = "¡Se ha aplicado el segundo aumento al semestre!"
        elif aumento == 3:
            incremento = Decimal('0.10')
            self.estudiante.semestre_a_pagar_estudiante += self.estudiante.valor_semestre_estudiante * incremento
            self.estudiante.aumento_3 = True
            mensaje = "¡Se ha aplicado el tercer aumento al semestre!"

        self.estudiante.save()
        messages.info(request, mensaje)




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


    # Crear instancia del observador del semestre y actualizar
    observador_semestre = ObservadorSemestre(usuario.estudiante, primera_financiera)
    observador_semestre.actualizar(request)

    # Obtener los mensajes y pasarlos al contexto
    mensajes = []
    for mensaje in messages.get_messages(request):
        mensajes.append(mensaje)

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
        'mensajes': mensajes,  # Agregar los mensajes al contexto
    })


def realizar_pago_semestre(request):
    if request.method == 'POST':
        opcion = request.POST.get('opcion')
        usuario = request.user.usuario
        estudiante = usuario.estudiante
        cuenta = usuario.cuenta

        if opcion == 'pago_total':
            saldo_suficiente = cuenta.saldo_usuario >= estudiante.valor_semestre_estudiante
            if saldo_suficiente:
                cuenta.saldo_usuario -= Decimal(estudiante.valor_semestre_estudiante)
                cuenta.save()
                estudiante.valor_semestre_estudiante = Decimal(0)
                estudiante.save()
                messages.success(request, '¡Pago realizado!')
            else:
                messages.error(request, 'Saldo insuficiente para realizar el pago total del semestre.')
        elif opcion == 'abono':
            valor_abono = request.POST.get('valor_abono')
            if valor_abono:
                valor_abono = Decimal(valor_abono)
                if valor_abono <= cuenta.saldo_usuario:
                    estudiante.valor_semestre_estudiante -= valor_abono
                    cuenta.saldo_usuario -= valor_abono
                    cuenta.save()
                    estudiante.save()
                    messages.success(request, '¡Abono realizado!')
                    if estudiante.valor_semestre_estudiante == Decimal(0):
                        messages.info(request, '¡Se ha completado el pago total del semestre!')
                else:
                    messages.error(request, 'Saldo insuficiente para realizar el abono.')
            else:
                messages.error(request, 'Ingrese un valor válido para el abono.')

    return redirect('consola_estudiantes')