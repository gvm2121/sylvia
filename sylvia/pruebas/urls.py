from django.urls import path
from . import views

urlpatterns = [
    path('inicio', views.index, name='index'),
    path('crear-pregunta', views.crear_pregunta, name='crear_pregunta'),
    path('crear-pregunta-procesar', views.crear_pregunta_procesar, name='crear_pregunta_procesar'),
    path('crear-prueba', views.crear_prueba, name='crear_prueba'),
    path('preguntas-guardadas', views.preguntas_guardadas, name='preguntas_guardadas'),
    path('crear-tag', views.crear_tags, name='crear_tag'),
    path('eliminar-tag/<int:tag_id>/', views.eliminar_tag, name='eliminar_tag'),
    path('guardar-tag', views.guardar_tags, name='guardar_tag'),
    path('salir', views.salir, name='salir'),
    path('generar-prueba', views.generar_prueba, name='generar_prueba'),
    path('editar/<int:unico_pregunta>/', views.preguntas_editadas, name="editar"),
    path('preguntas-guardadas-procesar', views.preguntas_guardadas_procesar, name='preguntas_guardadas_procesar'),
    path('guardar_pregunta_editada', views.guardar_pregunta_editada, name='guardar_pregunta_editada'),
    path('genera-pdf', views.generar_pdf, name='generar_pdf'),
    path('compartir', views.compartir, name='compartir'),
    path('compartir/usuario', views.compartir_usurio, name='compartir_usuario'),
    path('compartir/usuario/tags', views.guardar_compartidos_vista, name='guardar_compartido'),
    path('compartir/tabla-compartidos', views.tabla_compartidos, name='tabla_compartidos'),
    path('compartir/eliminar-permisos', views.eliminar_permiso, name='eliminar_permiso'),
    path('api/v1/<str:pregunta_numero>', views.api_traer_tag, name='api_traer_tag'),
    


    
    ]

