from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, logout, login
from datetime import date, timedelta
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date,datetime
from ast import Yield
from calendar import c
from pyexpat.errors import messages
from urllib import request
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, reverse
from django.urls import reverse_lazy
from django.forms import formset_factory, inlineformset_factory
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from .models import Socios,Planes,Subscripcion,Pago,Asistencia
from .forms import SociosForm, PlanesForm,SubscripcionForm,EditarPerfilForm,ProfesorForm
from django.utils.timezone import  localtime
from django.utils import timezone  
import pytz
from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib import messages




# Create your views here.
def index(request):
    return render(request,'index.html')

def navbar(request):
    return render(request, 'navbar.html')

def tabla_socios(request):
    socios = Socios.objects.all()
    context = {'socios': socios}
    return render(request, 'socios.html', context)

def tabla_planes(request):
    planes = Planes.objects.all()
    context = {'planes': planes}
    return render(request, 'planes.html', context)

def login_view(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request,'login.html', locals())

def home_view(request):
    if not request.user.is_staff:
        return redirect('login_view')
    
    p = Planes.objects.all().count()
    m = Socios.objects.all().count()

    d = { 'p': p, 'm': m}
    return render(request,'home.html', d)


#SOCIOS
class SociosLista(ListView):
    model = Socios
    template_name = 'socios.html'
    context_object_name = 'socios' 
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        socios = Socios.objects.all().order_by('-id')  

        if query:
            socios = socios.filter(
                Q(Nombre__icontains=query) |
                Q(Dni__icontains=query)
            )

        # 🔹 Agregar el saldo de cada socio antes de enviarlo al template
        for socio in socios:
            socio.saldo_actual = socio.obtener_saldo()  # Llamamos a la función para obtener el saldo

        return socios

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['m'] = Socios.objects.count()
        return context
    
    

class SociosNuevo(CreateView):
    model = Socios
    form_class = SociosForm
    template_name = 'frmSocios.html'
    success_url = reverse_lazy('SociosLista')

    def form_valid(self, form):
        # Después de guardar el nuevo socio, puedes redirigir o hacer algo más
        response = super().form_valid(form)
        return response

class SociosModif(UpdateView):
    model = Socios 
    form_class = SociosForm
    template_name = 'frmSocios.html'
    success_url = reverse_lazy('SociosLista')

class SociosBorrar(DeleteView):
    model = Socios
    template_name = 'borrarSocios.html'
    success_url = reverse_lazy('SociosLista')


#PLANES
class PlanesLista(ListView):
    model = Planes
    template_name = 'planes.html'
    context_object_name = 'planes'
    paginate_by = 5

    
    def get_queryset(self):
        query = self.request.GET.get('q', '')

        if not query:
            # Ordenar por ID descendente para que los últimos registros aparezcan primero
            planes = Planes.objects.all().order_by('-id')  
        else:
            planes = Planes.objects.filter(Nombre__icontains=query).order_by('-id')
        
        return planes
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['p'] = Planes.objects.count()  # Pasar el total de planes como 'p'
        return context

class PlanesNuevo(CreateView):
    model = Planes
    form_class = PlanesForm
    template_name = 'frmPlanes.html'
    success_url = reverse_lazy('PlanesLista')

class PlanesModif(UpdateView):
    model = Planes 
    form_class = PlanesForm
    template_name = 'frmPlanes.html'
    success_url = reverse_lazy('PlanesLista')

class PlanesBorrar(DeleteView):
    model = Planes
    template_name = 'borrarPlan.html'
    success_url = reverse_lazy('PlanesLista')


# def filtro_dinero(request):
#     total_ingresado = 0
#     error_message = None  # Variable para el mensaje de error
#     if request.method == "POST":
#         # Obtener las fechas desde el formulario
#         fecha_inicio_str = request.POST.get('fecha_inicio')
#         fecha_fin_str = request.POST.get('fecha_fin')

#         # Imprimir las fechas para depuración
#         print(f"Fecha inicio: {fecha_inicio_str}")
#         print(f"Fecha fin: {fecha_fin_str}")

#         try:
#             # Convertir las fechas a formato date
#             fecha_inicio = date.fromisoformat(fecha_inicio_str)
#             fecha_fin = date.fromisoformat(fecha_fin_str)

#             # Filtrar las subscripciones que hayan empezado dentro del rango de fechas
#             # Queremos las que tengan una fecha de inicio dentro del rango y, además, que no hayan terminado antes de la fecha de inicio.
#             subscripciones = Subscripcion.objects.filter(
#                 fecha_inicio__gte=fecha_inicio,  # Fecha de inicio mayor o igual a la fecha de inicio del filtro
#                 fecha_inicio__lte=fecha_fin      # Fecha de inicio menor o igual a la fecha de fin del filtro
#             )

#             # Sumar el monto total
#             total_ingresado = subscripciones.aggregate(Sum('monto'))['monto__sum'] or 0

#         except ValueError:
#             # Si las fechas no son válidas, mostrar un mensaje de error
#             error_message = "Por favor ingrese fechas válidas."

#     return render(request, 'filtro_dinero.html', {'total_ingresado': total_ingresado, 'error_message': error_message})


# Clave fija para ingresos (modifícala por seguridad)
CLAVE_INGRESOS = "30151182"

class ProteccionIngresosView(View):
    def get(self, request):
        return render(request, 'clave_ingresos.html')

    def post(self, request):
        clave_ingresada = request.POST.get('clave')

        if clave_ingresada == CLAVE_INGRESOS:
            request.session['acceso_ingresos'] = True
            return redirect('ingresos')  # Redirige a la vista de ingresos
        else:
            # messages.error( "Clave incorrecta. Intenta nuevamente.")
            return render(request, "clave_ingresos.html", {"error": True})  # Volver a mostrar el formulario sin redirigir

    
# class IngresosView(View):
#     def get(self, request):
#         if not request.session.get('acceso_ingresos'):
#             return redirect('proteger_ingresos')  # Si no tiene acceso, pide clave

#         return render(request, 'filtro_dinero.html', {'total_ingresado': 0, 'error_message': None})

#     def post(self, request):
#         if not request.session.get('acceso_ingresos'):
#             return redirect('proteger_ingresos')  

#         total_ingresado = 0
#         error_message = None  

#         fecha_inicio_str = request.POST.get('fecha_inicio')
#         fecha_fin_str = request.POST.get('fecha_fin')

#         try:
#             fecha_inicio = date.fromisoformat(fecha_inicio_str)
#             fecha_fin = date.fromisoformat(fecha_fin_str)

#             # Filtrar subscripciones en el rango de fechas
#             subscripciones = Subscripcion.objects.filter(
#                 fecha_inicio__gte=fecha_inicio,
#                 fecha_inicio__lte=fecha_fin
#             )

#             # Sumar el monto total
#             total_ingresado = subscripciones.aggregate(Sum('monto'))['monto__sum'] or 0

#         except ValueError:
#             error_message = "Por favor ingrese fechas válidas."

#         return render(request, 'filtro_dinero.html', {'total_ingresado': total_ingresado, 'error_message': error_message})

class IngresosView(View):
    def get(self, request):
        if not request.session.get('acceso_ingresos'):
            return redirect('proteger_ingresos')  # Si no tiene acceso, pide clave

        return render(request, 'filtro_dinero.html', {'total_ingresado_subs': 0, 'total_ingresado_saldos': 0, 'error_message': None})

    def post(self, request):
        if not request.session.get('acceso_ingresos'):
            return redirect('proteger_ingresos')  

        total_ingresado_subs = 0
        total_ingresado_saldos = 0
        error_message = None  

        fecha_inicio_str = request.POST.get('fecha_inicio')
        fecha_fin_str = request.POST.get('fecha_fin')

        try:
            fecha_inicio = date.fromisoformat(fecha_inicio_str)
            fecha_fin = date.fromisoformat(fecha_fin_str)

            # Filtrar subscripciones en el rango de fechas
            subscripciones = Subscripcion.objects.filter(
                fecha_inicio__gte=fecha_inicio,
                fecha_inicio__lte=fecha_fin
            )

            # Sumar el monto total de las subscripciones
            total_ingresado_subs = subscripciones.aggregate(Sum('monto'))['monto__sum'] or 0

            # Filtrar pagos de saldo dentro del rango de fechas
            pagos = Pago.objects.filter(
                fecha_pago__gte=fecha_inicio,
                fecha_pago__lte=fecha_fin
            )

            # Sumar el monto total de los pagos de saldo
            total_ingresado_saldos = pagos.aggregate(Sum('monto'))['monto__sum'] or 0

        except ValueError:
            error_message = "Por favor ingrese fechas válidas."

        # Pasar los totales de ambos ingresos al template
        total_ingresado = total_ingresado_subs + total_ingresado_saldos

        return render(request, 'filtro_dinero.html', {
            'total_ingresado_subs': total_ingresado_subs,
            'total_ingresado_saldos': total_ingresado_saldos,
            'total_ingresado': total_ingresado,
            'error_message': error_message
        })
#---------------------------------------------------------------------------------------------------------------

# SUBSCRIPCION    
class SubscripcionLista(ListView):
    model = Subscripcion
    template_name = 'subscripcion.html'
    context_object_name = 'subscripciones'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()  # Obtenemos el valor del buscador y eliminamos espacios
        if query:
            # Buscamos coincidencias en socio.Nombre, socio.Dni o plan.Nombre
            subscripciones = Subscripcion.objects.filter(
                Q(socio__Nombre__icontains=query) |
                Q(socio__Dni__icontains=query) |
                Q(plan__Nombre__icontains=query)
            ).order_by('-id')
        else:
            subscripciones = Subscripcion.objects.all().order_by('-id')
        return subscripciones

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = Socios.objects.count()  # Total de socios
        return context

class SubscripcionNuevo(CreateView):
    model = Subscripcion
    form_class = SubscripcionForm
    template_name = 'frmSubscripciones.html'
    success_url = reverse_lazy('SubscripcionLista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Verificar si 'socio_id' está en los parámetros de la URL
        socio_id = self.kwargs.get('socio_id')
        if socio_id:
            # Obtener el socio actual
            socio = Socios.objects.get(id=socio_id)

            # Pre-cargar el socio en el formulario
            context['form'].fields['socio'].initial = socio

            # Obtener el historial de suscripciones para este socio
            context['historial'] = Subscripcion.objects.filter(socio=socio).order_by('-id')

            # Agregar asistencias de este socio
            context['asistencias'] = Asistencia.objects.filter(subscripcion__socio=socio).order_by('-fecha_asistencia')

            # Agregar también las subscripciones (para el calendario)
            context['subscripciones'] = Subscripcion.objects.filter(socio=socio).order_by('-fecha_inicio')

            context['socio'] = socio  # Pasar también el socio al contexto por si lo necesitas
        else:
            context['historial'] = None
        return context

 #TRAE EL NOMBRE DEL SOCIO AL SELECCIONARLO
   # def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
        # Asegúrate de que 'socio_id' esté disponible y se pase al formulario
     #   if 'socio_id' in self.kwargs:
      #      socio = Socios.objects.get(id=self.kwargs['socio_id'])
       #     context['form'].fields['socio'].initial = socio  # Pre-cargar el socio en el formulario
       # return context
    
class SubscripcionModif(UpdateView):
    model = Subscripcion
    form_class = SubscripcionForm
    template_name = 'frmSubscripciones.html'
    success_url = reverse_lazy('SubscripcionLista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener el socio relacionado con la suscripción
        subscripcion = self.get_object()
        socio = subscripcion.socio
        
        # Agregar historial de suscripciones de ese socio al contexto
        context['historial'] = Subscripcion.objects.filter(socio=socio).order_by('-fecha_inicio')
        context['socio'] = socio  # Agregar también el socio al contexto

        # Obtener todas las asistencias del socio, no solo de la suscripción actual
        context['asistencias'] = Asistencia.objects.filter(subscripcion__socio=socio)

        #  Este era el que faltaba
        context['subscripciones'] = Subscripcion.objects.filter(socio=socio).order_by('-fecha_inicio')

        context['fechas_inicio_subs'] = list(
        Subscripcion.objects.filter(socio=socio).values_list('fecha_inicio', flat=True)
        )
        return context

class SubscripcionBorrar(DeleteView):
    model = Subscripcion
    template_name = 'borrarSubscripcion.html'
    success_url = reverse_lazy('SubscripcionLista')
        

def crear_suscripcion(request):
    if request.method == 'POST':
        form = SubscripcionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('SubscripcionLista')  # Cambia 'nombre_de_la_vista' por la vista a la que deseas redirigir
    else:
        form = SubscripcionForm()

    context = {'form': form}
    return render(request, 'frmSubscripciones.html', context)

 

   

#(registrar asistencia permitiendo descontar en negativo)
# def registrar_asistencia(request):
#     if request.method == "POST":
#         dni = request.POST.get("dni")  # Obtener el DNI del request


#         # Verificar si el socio existe
#         if not Socios.objects.filter(Dni=dni).exists():
#             return JsonResponse({
#                 "status": "error",
#                 "mensaje": "El socio con este DNI no existe."
#             })


#         # Buscar la suscripción del socio, incluso si está vencida o sin días
#         subscripcion = Subscripcion.objects.filter(
#             socio__Dni=dni  # Relación con el socio por DNI
#         ).order_by("-fecha_fin").first()  # Tomamos la última suscripción


#         if not subscripcion:
#             return JsonResponse({
#                 "status": "error",
#                 "mensaje": "El socio no tiene ninguna suscripción registrada."
#             })


#         # Determinar si la suscripción está vencida
#         vencida = now().date() > subscripcion.fecha_fin
#         sin_dias = subscripcion.dias <= 0


#         # Registrar la asistencia sin importar el estado de la suscripción
#         Asistencia.objects.create(subscripcion=subscripcion)


#         # Descontar un día, permitiendo valores negativos
#         subscripcion.dias -= 1
#         subscripcion.save()


#         # Construir mensaje de estado
#         mensaje = "Asistencia registrada."
#         if vencida and sin_dias:
#             mensaje = "La suscripción está vencida y no tiene días restantes."
#         elif vencida:
#             mensaje = "La suscripción está vencida."
#         elif sin_dias:
#             mensaje = "No tiene días restantes en su plan."

#         print("Saldo enviado al frontend:", subscripcion.saldo)
#         return JsonResponse({
#             "status": "success",
#             "nombre": subscripcion.socio.Nombre,  
#             "dias_restantes": subscripcion.dias,  # Puede ser negativo
#             "mensaje": mensaje,
#             "plan": subscripcion.plan.Nombre,
#             "vencimiento": subscripcion.fecha_fin,
#             "saldo": subscripcion.saldo,
#         })

def registrar_asistencia(request):
    if request.method == "POST":
        dni = request.POST.get("dni")  # Obtener el DNI del request

        # Verificar si el socio existe
        try:
            socio = Socios.objects.get(Dni=dni)  # Buscar al socio por su DNI
        except Socios.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "mensaje": "El socio con este DNI no existe."
            })

        # Buscar la suscripción del socio, incluso si está vencida o sin días
        subscripcion = Subscripcion.objects.filter(socio=socio).order_by("-fecha_fin").first()

        if not subscripcion:
            return JsonResponse({
                "status": "error",
                "mensaje": "El socio no tiene ninguna suscripción registrada."
            })

        # Determinar si la suscripción está vencida
        vencida = now().date() > subscripcion.fecha_fin
        sin_dias = subscripcion.dias <= 0

        # Registrar la asistencia sin importar el estado de la suscripción
        Asistencia.objects.create(subscripcion=subscripcion)

        # Descontar un día, permitiendo valores negativos
        subscripcion.dias -= 1
        subscripcion.save()

        # Construir mensaje de estado
        mensaje = "Asistencia registrada."
        if vencida and sin_dias:
            mensaje = "La suscripción está vencida y no tiene días restantes."
        elif vencida:
            mensaje = "La suscripción está vencida debe abonar su plan."
        elif sin_dias:
            mensaje = "No tiene días restantes en su plan."

        # Aquí estamos enviando el saldo desde la tabla Socios
        print("Saldo enviado al frontend:", socio.saldo_actual)

        return JsonResponse({
            "status": "success",
            "nombre": socio.Nombre,  # Nombre del socio
            "dias_restantes": subscripcion.dias,  # Días restantes en la suscripción
            "mensaje": mensaje,
            "plan": subscripcion.plan.Nombre,  # Nombre del plan
            "vencimiento": subscripcion.fecha_fin,  # Fecha de vencimiento de la suscripción
            "saldo": socio.saldo_actual,  # Traemos el saldo desde la tabla Socios
        })

    return JsonResponse({"status": "error", "mensaje": "Método no permitido."})


def asistencia_page(request):
    return render(request, 'asistencia.html')




def filtro_suscripciones(request):
    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")

    subscripciones = Subscripcion.objects.all()
    monto_total = 0

    if fecha_inicio and fecha_fin:
        # Filtrar las suscripciones por rango de fechas
        subscripciones = subscripciones.filter(
            fecha_inicio_gte=fecha_inicio, fecha_fin_lte=fecha_fin
        )
        # Calcular el monto total
        monto_total = subscripciones.aggregate(Sum('monto'))['monto__sum'] or 0

    return render(request, 'filtro_suscripciones.html', {
        'subscripciones': subscripciones,
        'monto_total': monto_total,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    })


def obtener_detalles_plan(request, plan_id):
    plan = Planes.objects.filter(id=plan_id).first()
    if plan:
        return JsonResponse({'monto': float(plan.Precio), 'dias': plan.Dias})
    return JsonResponse({'error': 'Plan no encontrado'}, status=404)

def obtener_detalles_socio(request, socio_id):
    socio = Socios.objects.filter(id=socio_id).first()
    if socio:
        return JsonResponse({
            'dni': socio.Dni,
            'nombre': f"{socio.Nombre}"
        })
    return JsonResponse({'error': 'Socio no encontrado'}, status=404)


#------------------------------------------------------------------------------
def perfil_actualizado(request):
    return render(request, 'perfil_actualizado.html')

class EditarPerfilView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditarPerfilForm
    template_name = 'editar_perfil.html'
    success_url = reverse_lazy('perfil_actualizado')

    def get_object(self):
        return self.request.user  # Devuelve el usuario logueado
    
    

##PROFESORES------------------------------------------------------------------------
class ProfesorLista(ListView):
    model = Profesor
    template_name = 'profesor.html'
    context_object_name = 'profesor'
    paginate_by = 5


    def get_queryset(self):
        query = self.request.GET.get('q', '')


        if not query:
            # Ordenar por ID descendente para que los últimos registros aparezcan primero
            profesor = Profesor.objects.all().order_by('-id')  
        else:
            profesor = Profesor.objects.filter(nombre__icontains=query).order_by('-id')
       
        return profesor


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['f'] = Profesor.objects.count()  # Pasar el total de socios como 'm'
        return context


class ProfesorNuevo(CreateView):
    model = Profesor
    form_class = ProfesorForm
    template_name = 'frmProfesor.html'
    success_url = reverse_lazy('ProfesorLista')


    def form_valid(self, form):
        # Después de guardar el nuevo socio, puedes redirigir o hacer algo más
        response = super().form_valid(form)
        return response


class ProfesorModif(UpdateView):
    model = Profesor
    form_class = ProfesorForm
    template_name = 'frmProfesor.html'
    success_url = reverse_lazy('ProfesorLista')


class ProfesorBorrar(DeleteView):
    model = Profesor
    template_name = 'borrarProfesor.html'
    success_url = reverse_lazy('ProfesorLista')

class RegistrarIngresoEgreso(View):
    def post(self, request):
        dni = request.POST.get("dni")


        # Validar que el DNI pertenece a un profesor
        profesor = Profesor.objects.filter(dni=dni).first()
        if not profesor:
            return JsonResponse({
                "status": "error",
                "mensaje": "El profesor con este DNI no existe."
            })


        # Verificar si el profesor ya tiene un registro de ingreso sin egreso
        registro = RegistroIngresoEgreso.objects.filter(profesor=profesor, fecha_hora_egreso__isnull=True).first()


        if registro:
            # Registrar salida
            registro.fecha_hora_egreso = timezone.now()
            registro.save()


            hora_salida = timezone.localtime(registro.fecha_hora_egreso).strftime("%H:%M:%S")
            hora_ingreso = timezone.localtime(registro.fecha_hora_ingreso).strftime("%H:%M:%S")


            return JsonResponse({
                "status": "success",
                "mensaje": f"Egreso registrado para {profesor.nombre}.",
                "nombre_profesor": profesor.nombre,
                "hora_ingreso": hora_ingreso,
                "hora_salida": hora_salida if registro.fecha_hora_egreso else "No registrado"
            })
        else:
            # Registrar ingreso
            nuevo_registro = RegistroIngresoEgreso.objects.create(profesor=profesor, fecha_hora_ingreso=timezone.localtime())
            return JsonResponse({
                "status": "success",
                "mensaje": f"Ingreso registrado {profesor.nombre}.",
                "nombre_profesor": profesor.nombre,
                "hora_ingreso": nuevo_registro.fecha_hora_ingreso.strftime("%H:%M:%S")
            })


    def get(self, request):
        return JsonResponse({"status": "error", "mensaje": "Método no permitido."})
   


def registro_page(request):
    return render(request, 'registro.html')


def ListarSociosIngresados(request):
    fecha_str = request.GET.get("fecha")
   
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date() if fecha_str else datetime.today().date()
    except ValueError:
        return JsonResponse({"error": "Formato de fecha inválido"}, status=400)


    asistencias = Asistencia.objects.filter(fecha_asistencia__date=fecha).order_by('-fecha_asistencia')


    paginator = Paginator(asistencias, 10)  # Paginación
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)


    local_tz = pytz.timezone('America/Argentina/Buenos_Aires')


    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        registros = [
            {
                "nombre": asistencia.subscripcion.socio.Nombre,
                "fecha": asistencia.fecha_asistencia.strftime("%d/%m/%Y"),
                "hora_ingreso": asistencia.fecha_asistencia.astimezone(local_tz).strftime("%H:%M:%S"),
                "suscripcion_vencida": asistencia.subscripcion.dias <= 0 or asistencia.subscripcion.fecha_fin < datetime.today().date()
            }
            for asistencia in page_obj
        ]
        return JsonResponse({
            "status": "success",
            "registros": registros,
            "paginacion": render_to_string('paginacion.html', {'page_obj': page_obj}),
        })


    return render(request, "listar_socios_ingresados.html", {"page_obj": page_obj, "hoy": datetime.today().strftime("%Y-%m-%d")})


#Listado de profesor con sus ingresos
def ListarProfesoresIngresados(request):
    # Obtener la fecha de la solicitud
    fecha_str = request.GET.get("fecha")
   
    try:
        # Si la fecha está en la solicitud, la convertimos; si no, usamos la fecha actual
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date() if fecha_str else datetime.today().date()
    except ValueError:
        return JsonResponse({"error": "Formato de fecha inválido"}, status=400)


    # Filtrar los registros de ingreso y egreso en la fecha seleccionada
    registros = RegistroIngresoEgreso.objects.filter(fecha_hora_ingreso__date=fecha).order_by('-fecha_hora_ingreso')


    # PAGINACIÓN: Agregar paginador
    paginator = Paginator(registros, 10)  # 10 registros por página
    page_number = request.GET.get("page")  # Obtener número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtener la página solicitada


    # Zona horaria local (ajústala según tu necesidad)
    local_tz = pytz.timezone('America/Argentina/Buenos_Aires')


    # Si la solicitud es una petición AJAX
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        # Estructura la respuesta JSON, convirtiendo las horas a la hora local
        datos = [
            {
                "profesor": registro.profesor.nombre,
                "fecha": registro.fecha_hora_ingreso.strftime("%d/%m/%Y"),  # Fecha en formato DD/MM/YYYY
                "hora_ingreso": registro.fecha_hora_ingreso.astimezone(local_tz).strftime("%H:%M:%S"),  # Hora de ingreso en hora local
                "hora_salida": registro.fecha_hora_egreso.astimezone(local_tz).strftime("%H:%M:%S") if registro.fecha_hora_egreso else "No registrado"
            }
            for registro in page_obj
        ]
        # Devuelve los registros y la paginación en formato JSON
        return JsonResponse({
            "status": "success",
            "registros": datos,
            "paginacion": render_to_string('paginacion.html', {'page_obj': page_obj}),  # Renderiza los controles de paginación # type: ignore
           
        })


    # Para la vista inicial (sin AJAX), renderiza los registros y la fecha actual
    return render(request, "detallesRegistro.html", {"page_obj": page_obj, "hoy": datetime.today().strftime("%Y-%m-%d")})


class FiltrarAsistenciaSociosView(View):
    def get(self, request):
        fecha_str = request.GET.get("fecha")
       
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return JsonResponse({"status": "error", "mensaje": "Formato de fecha inválido."})
       
        asistencias = Asistencia.objects.filter(fecha_asistencia__date=fecha).select_related("subscripcion__socio")
       
        if not asistencias.exists():
            return JsonResponse({"status": "error", "mensaje": "No hay registros para esta fecha."})
       
        registros = [
            {
                "socio": asistencia.subscripcion.socio.Nombre,
                "hora_ingreso": asistencia.fecha_asistencia.strftime("%H:%M:%S"),
                "plan": asistencia.subscripcion.plan.Nombre
            }
            for asistencia in asistencias
        ]
       
        return JsonResponse({"status": "success", "registros": registros})

#Filtrar asistencia de profes
class FiltrarAsistenciaProfesoresView(View):
    def get(self, request):
        fecha_str = request.GET.get("fecha")


        if fecha_str:
            try:
                fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                return JsonResponse({"status": "error", "mensaje": "Formato de fecha inválido."})
        else:
            fecha = localtime()  # Si no se ingresa fecha, toma la del día actual


        registros = RegistroIngresoEgreso.objects.filter(fecha_hora_ingreso__date=fecha).select_related("profesor")


        if not registros.exists():
            return JsonResponse({"status": "error", "mensaje": "No hay registros para esta fecha."})


        resultado = [
            {
                "profesor": registro.profesor.nombre,
                "hora_ingreso": registro.fecha_hora_ingreso.strftime("%H:%M:%S"),
                "hora_salida": registro.fecha_hora_egreso.strftime("%H:%M:%S") if registro.fecha_hora_egreso else "No registrado"
            }
            for registro in registros
        ]


        return JsonResponse({"status": "success", "registros": resultado})

#Registra cuando un socio paga su saldo--------------------------------------------------------
# Vista para registrar pagos

# class RegistrarPagoView(View):
#     def get(self, request, subscripcion_id):
#         # Obtener la subscripción específica para mostrar al usuario (aunque no es crucial para el pago total)
#         subscripcion = get_object_or_404(Subscripcion, id=subscripcion_id)
        
#         # Obtener el socio relacionado con la subscripción
#         socio = subscripcion.socio
        
#         # Calcular la deuda total de todas las suscripciones del socio
#         deuda_total = socio.subscripcion_set.filter(saldo__gt=0).aggregate(total=Sum('saldo'))['total'] or Decimal(0)

#         return render(request, 'registrar_pago.html', {
#             'subscripcion': subscripcion,
#             'deuda_total': deuda_total
#         })

#     def post(self, request, subscripcion_id):
#         # Obtener la subscripción específica para mostrar al usuario
#         subscripcion = get_object_or_404(Subscripcion, id=subscripcion_id)
        
#         # Obtener el socio relacionado con la subscripción
#         socio = subscripcion.socio
        
#         # Obtener el monto del pago
#         monto_pago = Decimal(request.POST.get('monto', 0))

#         if monto_pago > 0:
#             # Restar el pago del saldo de todas las subscripciones del socio
#             subscripciones_con_deuda = socio.subscripcion_set.filter(saldo__gt=0)
            
#             for subscripcion in subscripciones_con_deuda:
#                 if monto_pago <= 0:
#                     break  # Si ya no queda dinero para pagar, salimos del loop
                
#                 # Si el monto del pago es mayor que el saldo de la subscripción, pagamos todo
#                 if subscripcion.saldo <= monto_pago:
#                     monto_pago -= subscripcion.saldo
#                     subscripcion.saldo = Decimal(0)
#                 else:
#                     # Si el monto del pago es menor, pagamos parte de la subscripción
#                     subscripcion.saldo -= monto_pago
#                     monto_pago = Decimal(0)
                
#                 subscripcion.save()

#             # Calcular la nueva deuda total
#             deuda_total = socio.subscripcion_set.filter(saldo__gt=0).aggregate(total=Sum('saldo'))['total'] or Decimal(0)
#             socio.saldo_actual = deuda_total
#             socio.save()

#         return redirect('socios_con_deuda')


class RegistrarPagoView(View):
    def get(self, request, subscripcion_id):
        # Intentar obtener la subscripción
        try:
            subscripcion = get_object_or_404(Subscripcion, id=subscripcion_id)
        except Subscripcion.DoesNotExist:
            return redirect('subscripcion/SubscripcionLista')

        socio = subscripcion.socio

        # Calcular la deuda total del socio
        deuda_total = socio.subscripcion_set.filter(saldo__gt=0).aggregate(total=Sum('saldo'))['total'] or Decimal(0)

        return render(request, 'registrar_pago.html', {
            'socio': socio,
            'deuda_total': deuda_total
        })

    def post(self, request, subscripcion_id):
        subscripcion = get_object_or_404(Subscripcion, id=subscripcion_id)
        socio = subscripcion.socio

        # Calcular la deuda total actual del socio
        deuda_total = socio.subscripcion_set.filter(saldo__gt=0).aggregate(total=Sum('saldo'))['total'] or Decimal(0)

        # Obtener el monto ingresado
        monto_pago = request.POST.get('monto', 0)

        try:
            monto_pago = Decimal(monto_pago)
        except Exception:
            monto_pago = Decimal(0) 

        # 🔒 VALIDACIÓN: no permitir pago mayor que la deuda
        if monto_pago > deuda_total:
            messages.error(request, f"El monto ingresado ${monto_pago} supera la deuda total. Corrígelo antes de continuar.")
            return redirect(request.META.get('HTTP_REFERER', 'subscripcion/SubscripcionLista'))
       

        if monto_pago > 0:
            monto_pago_inicial = monto_pago
            subscripciones_con_deuda = socio.subscripcion_set.filter(saldo__gt=0)

            for subscripcion in subscripciones_con_deuda:
                if monto_pago <= 0:
                    break
                if subscripcion.saldo <= monto_pago:
                    monto_pago -= subscripcion.saldo
                    subscripcion.saldo = Decimal(0)
                else:
                    subscripcion.saldo -= monto_pago
                    monto_pago = Decimal(0)
                subscripcion.save()

            deuda_total = socio.subscripcion_set.filter(saldo__gt=0).aggregate(total=Sum('saldo'))['total'] or Decimal(0)
            socio.saldo_actual = deuda_total
            socio.save()

            if monto_pago_inicial > 0:
                Pago.objects.create(socio=socio, monto=monto_pago_inicial, fecha_pago=date.today())
                messages.success(request, f"Pago de ${monto_pago_inicial} registrado correctamente.")
        else:
            messages.error(request, "Debe ingresar un monto válido mayor que 0.")

        return redirect('socios_con_deuda', socio_id=socio.id)

# Vista para listar socios con deuda
class SociosConDeudaView(ListView):
    model = Socios
    template_name = 'socios_con_deuda.html'
    context_object_name = 'socios_con_deuda'
    paginate_by = 5  # Asegúrate de usar un número entero

    def get_queryset(self):
        query = self.request.GET.get('q', '')  # Obtener el término de búsqueda

        # Anotar la deuda total de todas las suscripciones de un mismo socio
        socios_con_deuda = Socios.objects.annotate(
            deuda_total=Sum('subscripcion__saldo', filter=Q(subscripcion__saldo__gt=0))
        ).filter(deuda_total__gt=0)  # Filtrar solo socios con deuda mayor a 0
        
        if query:
            socios_con_deuda = socios_con_deuda.filter(
                Q(Nombre__icontains=query) | Q(Dni__icontains=query)
            )
        return socios_con_deuda

    def get_context_data(self, **kwargs):
        # Obtiene el contexto base
        context = super().get_context_data(**kwargs)

        # Sumar las deudas de todos los socios con deuda
        total_deuda = Socios.objects.annotate(
            deuda_total=Sum('subscripcion__saldo', filter=Q(subscripcion__saldo__gt=0))
        ).filter(deuda_total__gt=0).aggregate(total=Sum('deuda_total'))['total'] or 0

        # Pasar la suma total de la deuda al contexto
        context['total_deuda'] = total_deuda
        context['query'] = self.request.GET.get('q', '')  # Para mantener el término en el input

        return context

class RegistroPagoLista(ListView):
    model = Pago
    template_name = 'Registro_Pago_Lista.html'
    context_object_name = 'pagos'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:  
            return Pago.objects.filter(socio__Nombre__icontains=query).order_by('-id')
        return Pago.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['p'] = Pago.objects.count()
        print("Contexto generado:", context)  # <-- Esto imprimirá el contexto en la consola
        return context

 

