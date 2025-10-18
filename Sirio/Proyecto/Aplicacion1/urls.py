from django.contrib import admin
from django.urls import path
from. import views
from django.views.generic import TemplateView
from .views import EditarPerfilView  # Importar la vista correctamente
from .views import perfil_actualizado

urlpatterns = [ 
    path('', views.index, name='index'),
    path('navbar/', views.navbar, name='navbar'),
    path('cerrar/', TemplateView.as_view(template_name='cerrar.html'), name='cerrar'),

    #path('filtro-dinero/', views.FiltroDineroView.as_view(), name='filtro_dinero'),
    # path('proteger-ingresos/', views.ProteccionIngresosView.as_view(), name='proteger_ingresos'),

    path('proteger-ingresos/', views.ProteccionIngresosView.as_view(), name='proteger_ingresos'),
    path('ingresos/', views.IngresosView.as_view(), name='ingresos'),

   

    path('socios/', views.tabla_socios, name='socios'),
    path('planes /', views.tabla_planes, name='planes'),
    path('login_view/', views.login_view, name='login_view'),
    path('home_view', views.home_view , name='home_view'),


     path('socios/SociosLista/', views.SociosLista.as_view(), name='SociosLista'),
     path('socios/SociosNuevo/', views.SociosNuevo.as_view(), name='SociosNuevo'),
     path('socios/SociosModif/<int:pk>/', views.SociosModif.as_view(), name='SociosModif'),
     path('socios/SociosBorrar/<int:pk>/', views.SociosBorrar.as_view(), name='SociosBorrar'),

     path('planes/PlanesLista/', views.PlanesLista.as_view(), name='PlanesLista'),
     path('planes/PlanesNuevo/', views.PlanesNuevo.as_view(), name='PlanesNuevo'),
     path('planes/PlanesModif/<int:pk>/', views.PlanesModif.as_view(), name='PlanesModif'),
     path('planes/PlanesBorrar/<int:pk>/', views.PlanesBorrar.as_view(), name='PlanesBorrar'),


    path('subscripcion/SubscripcionLista/', views.SubscripcionLista.as_view(), name='SubscripcionLista'),
    path('subscripcion/SubscripcionNuevo/<int:socio_id>/', views.SubscripcionNuevo.as_view(), name='SubscripcionNuevo'),
    path('subscripcion/SubscripcionModif/<int:pk>/', views.SubscripcionModif.as_view(), name='SubscripcionModif'),
    path('subscripcion/SubscripcionBorrar/<int:pk>/', views.SubscripcionBorrar.as_view(), name='SubscripcionBorrar'),
    

    path('asistencia/', views.asistencia_page, name='asistencia_page'),  # Página de asistencia
    path('registrar_asistencia/', views.registrar_asistencia, name='registrar_asistencia'),  # Endpoint de registro

     path('filtro_suscripciones/', views.filtro_suscripciones, name='filtro_suscripciones'),

     path('crear_suscripcion/', views.crear_suscripcion, name='crear_suscripcion'),
     path('obtener_detalles_plan/<int:plan_id>/', views.obtener_detalles_plan, name='obtener_detalles_plan'),
     path('obtener_detalles_socio/<int:socio_id>/', views.obtener_detalles_socio, name='obtener_detalles_socio'),


    path('editar-perfil/', EditarPerfilView.as_view(), name='editar_perfil'),
    path('perfil-actualizado/', perfil_actualizado, name='perfil_actualizado'),


    path('profesor/ProfesorLista/', views.ProfesorLista.as_view(), name='ProfesorLista'),
    path('profesor/ProfesorNuevo/', views.ProfesorNuevo.as_view(), name='ProfesorNuevo'),
    path('profesor/ProfesorModif/<int:pk>/', views.ProfesorModif.as_view(), name='ProfesorModif'),
    path('profesor/ProfesorBorrar/<int:pk>/', views.ProfesorBorrar.as_view(), name='ProfesorBorrar'),
    
    #Registro de profesores
    path('registro/', views.registro_page, name='registro_page'),  # Página de registro
    path('registro_profesor/', views.RegistrarIngresoEgreso.as_view(), name='registro_profesor'), # Endpoint de registro
    path('socios_ingresados/', views.ListarSociosIngresados, name='ListarSociosIngresados'),
    #path('socios_ingresados/', views.ListarSociosIngresadosView.as_view(), name='listar_socios_ingresados'),
    path('profesor_ingresados/', views.ListarProfesoresIngresados, name='ListarProfesoresIngresados'),

    path('socios_con_deuda/<int:socio_id>', views.SociosConDeudaView.as_view(), name='socios_con_deuda'),
      path('socios_con_deuda/', views.SociosConDeudaView.as_view(), name='socios_con_deuda'),  # Nueva ruta para socios con deuda
    path('registrar_pago/<int:subscripcion_id>/', views.RegistrarPagoView.as_view(), name='registrar_pago'),

    path('RegistroPagoLista/', views.RegistroPagoLista.as_view(), name='RegistroPagoLista'),
    ]

