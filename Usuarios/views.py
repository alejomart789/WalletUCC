import decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from Usuarios.models import Financiera
from datetime import date, datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from Usuarios.models import Usuario, Estudiante, Financiera, Transaccion
from dateutil import parser




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
            self.estudiante.valor_semestre_estudiante += self.estudiante.valor_semestre_estudiante * incremento
            self.estudiante.aumento_2 = True
            mensaje = "¡Se ha aplicado el segundo aumento al semestre!"
        elif aumento == 3:
            incremento = Decimal('0.10')
            self.estudiante.valor_semestre_estudiante += self.estudiante.valor_semestre_estudiante * incremento
            self.estudiante.aumento_3 = True
            mensaje = "¡Se ha aplicado el tercer aumento al semestre!"

        self.estudiante.save()
        messages.info(request, mensaje)


def login_user(request):
    if request.user.is_authenticated:
        usuario = Usuario.objects.get(user=request.user)

        if Estudiante.objects.filter(usuario=usuario).exists():
            return redirect('consola_estudiantes')

        if Financiera.objects.filter(usuario=request.user).exists():
            return redirect('consola_financiera')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            usuario = Usuario.objects.get(user=user)
            if Estudiante.objects.filter(usuario=usuario).exists():
                return redirect('consola_estudiantes')

            if Financiera.objects.filter(usuario=user).exists():
                return redirect('consola_financiera')

        error_message = 'Usuario o contraseña inválidos'
        return render(request, 'Usuarios/login.html', {'error_message': error_message})
    
    return render(request, 'Usuarios/login.html')


# Lo que se llama cada vez que se recarga la consola estudiantes
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
    
    foto_perfil = f"{usuario.foto_perfil}"

    context = {
        'fecha_actual': fecha_actual,
        'nombre_completo': nombre_completo,
        'saldo': saldo,
        'saldo_str': saldo_str,
        'semestre_pagar': semestre_pagar,
        'valor_semestre_str': valor_semestre_str,
        'fechas_limites_pago': fechas_limites_pago,
        'mensajes': mensajes,
        'foto_perfil': foto_perfil
    }

    return render(request, 'Estudiantes/consola_estudiantes.html', context)


@login_required
def actualizar_perfil(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        foto_perfil = request.FILES.get('foto_perfil')

        usuario = request.user.usuario
        usuario.email = email

        if foto_perfil:
            # Validar que el archivo sea de tipo PNG
            if not foto_perfil.name.lower().endswith('.png'):
                return redirect('perfil_estudiante')

            # Guardar la foto de perfil en el campo 'foto_perfil' del modelo
            usuario.foto_perfil.save(foto_perfil.name, foto_perfil)

        usuario.save()

    return redirect('perfil_estudiante')

@login_required
def perfil_estudiante(request):
    usuario = request.user.usuario

    nombre_completo = f"{usuario.nombres} {usuario.apellidos}"
    nombre = f"{usuario.nombres}"
    apellidos = f"{usuario.apellidos}"
    
    email = f"{usuario.email}"
    foto_perfil = f"{usuario.foto_perfil}"
    
    identificacion = f"{usuario.identificacion}"

    return render(request, 'Estudiantes/perfil_estudiante.html', {
        'nombre_completo': nombre_completo,
        'nombre' : nombre,
        'apellidos': apellidos,
        'email': email,
        'foto_perfil': foto_perfil,
        'identificacion': identificacion,
    })


@login_required
def perfil_financiera(request):
    usuario = request.user.usuario

    nombre_completo = f"{usuario.nombres} {usuario.apellidos}"
    nombre = f"{usuario.nombres}"
    apellidos = f"{usuario.apellidos}"
    
    email = f"{usuario.email}"
    foto_perfil = f"{usuario.foto_perfil}"
    
    identificacion = f"{usuario.identificacion}"

    return render(request, 'Financiera/perfil_financiera.html', {
        'nombre_completo': nombre_completo,
        'nombre' : nombre,
        'apellidos': apellidos,
        'email': email,
        'foto_perfil': foto_perfil,
        'identificacion': identificacion,
    })

@login_required
def actualizar_perfil_financiera(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        foto_perfil = request.FILES.get('foto_perfil')

        usuario = request.user.usuario
        usuario.email = email

        if foto_perfil:
            # Validar que el archivo sea de tipo PNG
            if not foto_perfil.name.lower().endswith('.png'):
                return redirect('perfil_financiera')

            # Guardar la foto de perfil en el campo 'foto_perfil' del modelo
            usuario.foto_perfil.save(foto_perfil.name, foto_perfil)

        usuario.save()

    return redirect('perfil_financiera')


@login_required
def consola_financiera(request):
    usuario = request.user.usuario
    financiera = Financiera.objects.first()

    if request.method == 'POST':
        fecha_limite_pago_1 = request.POST.get('fecha_limite_pago_1')
        fecha_limite_pago_2 = request.POST.get('fecha_limite_pago_2')
        fecha_limite_pago_3 = request.POST.get('fecha_limite_pago_3')

        financiera.fecha_limite_pago_1 = fecha_limite_pago_1
        financiera.fecha_limite_pago_2 = fecha_limite_pago_2
        financiera.fecha_limite_pago_3 = fecha_limite_pago_3

        financiera.save()

        return redirect('consola_financiera')

    nombre_completo = f"{usuario.nombres} {usuario.apellidos}"
    nombre = f"{usuario.nombres}"
    apellidos = f"{usuario.apellidos}"
    email = f"{usuario.email}"
    foto_perfil = f"{usuario.foto_perfil}"
    identificacion = f"{usuario.identificacion}"
    
    saldo = financiera.saldo_financiera
    saldo_str = f"{saldo:,}"

    # Convertir las fechas al formato "yyyy-MM-dd"
    fecha_limite_pago_1_str = financiera.fecha_limite_pago_1.strftime('%Y-%m-%d')
    fecha_limite_pago_2_str = financiera.fecha_limite_pago_2.strftime('%Y-%m-%d')
    fecha_limite_pago_3_str = financiera.fecha_limite_pago_3.strftime('%Y-%m-%d')

    return render(request, 'Financiera/consola_financiera.html', {
        'nombre_completo': nombre_completo,
        'nombre': nombre,
        'apellidos': apellidos,
        'email': email,
        'foto_perfil': foto_perfil,
        'identificacion': identificacion,
        'saldo_str': saldo_str,
        'fecha_limite_pago_1': fecha_limite_pago_1_str,
        'fecha_limite_pago_2': fecha_limite_pago_2_str,
        'fecha_limite_pago_3': fecha_limite_pago_3_str,
    })
    
@login_required
def transacciones_financiera(request):
    estudiantes = Estudiante.objects.all()
    nombres_apellidos_estudiantes = [f"{estudiante.usuario.nombres} {estudiante.usuario.apellidos}" for estudiante in estudiantes]
        
    transacciones = Transaccion.objects.all()  # Obtener todas las transacciones sin filtrar
    
    if request.method == 'POST':
        origen = 'Financiera'
        financiera = request.user.financiera
        destino_id = request.POST['destino']
        informacion_transaccion = request.POST['informacion_transaccion']
        descripcion = request.POST['descripcion']
        valor_transaccion = request.POST['valor_transaccion']
        monto_transaccion = request.POST['monto_transaccion']
        fecha_vencimiento = request.POST['fecha_vencimiento']

        destino = Estudiante.objects.get(id=destino_id)

        if informacion_transaccion == 'Pago de Semestre':
            # Crear la transacción
            transaccion = Transaccion(
                origen=origen,
                financiera=financiera,
                destino=destino,
                informacion_transaccion=informacion_transaccion,
                descripcion=descripcion,
                valor_transaccion=valor_transaccion,
                monto_transaccion=monto_transaccion,
                fecha_vencimiento_transaccion=fecha_vencimiento
            )
            transaccion.save()

            # Actualizar el valor a pagar del semestre del estudiante
            destino.valor_semestre_estudiante += Decimal(valor_transaccion)
            destino.save()

    return render(request, 'Financiera/transacciones_financiera.html', {
        'nombres_apellidos_estudiantes': nombres_apellidos_estudiantes,
        'estudiantes': estudiantes, 
        'transacciones': transacciones,
    })

