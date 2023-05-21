from abc import ABC, abstractmethod
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from Usuarios.models import Financiera
from datetime import date, datetime
from decimal import Decimal

import locale

class Observable:
    def __init__(self):
        self.observadores = []

    def agregar_observador(self, observador):
        self.observadores.append(observador)

    def eliminar_observador(self, observador):
        self.observadores.remove(observador)

    def notificar_observadores(self, evento):
        for observador in self.observadores:
            observador.actualizar(evento)

class Observador(ABC):
    @abstractmethod
    def actualizar(self, evento):
        pass

class ObservadorAumentoSemestre(Observador):
    def __init__(self, estudiante, request):
        self.estudiante = estudiante
        self.request = request

    def actualizar(self, evento):
        fecha_actual = evento['fecha_actual']
        financiera = evento['financiera']

        if fecha_actual > financiera.fecha_limite_pago_1 and not self.estudiante.aumento_1:
            self.estudiante.valor_semestre_estudiante *= Decimal(1.02)  # Aumento del 2%
            self.estudiante.aumento_1 = True
            self.estudiante.save()

            # Enviar notificación al estudiante
            mensaje = 'Se ha aplicado un aumento del 2% al valor del semestre.'
            self.enviar_notificacion(mensaje)

        if fecha_actual > financiera.fecha_limite_pago_2 and not self.estudiante.aumento_2:
            self.estudiante.valor_semestre_estudiante *= Decimal(1.05)  # Aumento del 5%
            self.estudiante.aumento_2 = True
            self.estudiante.save()

            # Enviar notificación al estudiante
            mensaje = 'Se ha aplicado un aumento del 5% al valor del semestre.'
            self.enviar_notificacion(mensaje)

        if fecha_actual > financiera.fecha_limite_pago_3 and not self.estudiante.aumento_3:
            self.estudiante.valor_semestre_estudiante *= Decimal(1.05)  # Aumento del 5%
            self.estudiante.aumento_3 = True
            self.estudiante.save()

            # Enviar notificación al estudiante
            mensaje = 'Se ha aplicado un aumento del 5% al valor del semestre.'
            self.enviar_notificacion(mensaje)

    def enviar_notificacion(self, mensaje):
        # Utilizar el framework de mensajes para mostrar la notificación
        messages.info(self.request, mensaje)


# Autenticación de usuario
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

# Vista de la consola de estudiantes
@login_required
def consola_estudiantes(request):
    fecha_actual = date.today()
    usuario = request.user.usuario

    financiera = Financiera.objects.first()

    estudiante = usuario.estudiante
    observador_aumento_semestre = ObservadorAumentoSemestre(estudiante, request)

    

    observable = Observable()
    observable.agregar_observador(observador_aumento_semestre)
    
    evento = {
    'fecha_actual': fecha_actual,
    'financiera': financiera,
    }

    # Eliminar las notificaciones más antiguas después de 24 horas
    messages.get_messages(request).expire_seconds = 86400
    
    observable.notificar_observadores(evento)


    # Fechas límites de pago que el estudiante tiene para pagar el semestre
    fechas_limites_pago = [
        financiera.fecha_limite_pago_1,
        financiera.fecha_limite_pago_2,
        financiera.fecha_limite_pago_3
    ]



    # Se traen los datos del usuario
    nombre_completo = f"{usuario.nombres} {usuario.apellidos}"
    saldo = usuario.cuenta.saldo_usuario
    saldo_str = locale.format_string('%.2f', saldo, grouping=True)
    semestre_pagar = usuario.estudiante.semestre_a_pagar_estudiante
    valor_semestre_str = locale.format_string('%.2f', usuario.estudiante.valor_semestre_estudiante, grouping=True)

    return render(request, 'Estudiantes/consola_estudiantes.html', {
    'nombre_completo': nombre_completo,
    'saldo_str': saldo_str,
    'semestre_pagar': semestre_pagar,
    'valor_semestre_str': valor_semestre_str,
    'fechas_limites_pago': fechas_limites_pago,
    'fecha_actual': fecha_actual,
    'messages': list(messages.get_messages(request)),
    })

