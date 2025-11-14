from django.urls import path
from . import views
from .views import (ListaGradosView, CrearGradoView, EditarGradoView, EliminarGradoView, EditarEstadoAnioView,
                    CrearMateriaView, EditarMateriaView, EliminarMateriaView, )     

app_name = 'notas'

urlpatterns = [
    
    # Escalas de notas
    path('escalas', views.EscalaNotaListView.as_view(), name='escala_lista'),
    path('nuevaescalas/crear/', views.EscalaNotaCreateView.as_view(), name='escala_nueva'),
    path('escalas/<int:pk>/editar/', views.EscalaNotaUpdateView.as_view(), name='escala_editar'),
    path('escalas/<int:pk>/eliminar/', views.EscalaNotaDeleteView.as_view(), name='escala_eliminar'),

    # Años escolares
    path('anios/crear/', views.AnioEscolarCreateView.as_view(), name='crear_anio'),
    #path('anios/', views.gestionar_anios_periodos, name='lista_anios'),
    #path('anios/<int:pk>/editar-estado/', views.editar_estado_anio, name='editar_estado_anio'),
    path('anio-escolar/editar-estado/<int:pk>/', EditarEstadoAnioView.as_view(), name='editar_estado_anio'),
    path('anio-escolar/eliminar/<int:pk>/', views.EliminarAnioEscolarView.as_view(), name='eliminar_anio'),
    path('anios-periodos/', views.GestionarAniosPeriodosView.as_view(), name='lista_anios'),
    
    # Períodos
    path('periodos/', views.ListaPeriodosView.as_view(), name='lista_periodos'),
    path('periodos/crear/', views.CrearPeriodoView.as_view(), name='crear_periodo'),
    path('periodos/eliminar/<int:pk>/', views.EliminarPeriodoView.as_view(), name='eliminar_periodo'),
    #path('anios-periodos/', GestionarAniosPeriodosView.as_view(), name='lista_anios'),
    
    # API para filtrado dinámico
    path('api/periodos-por-anio/<int:anio_id>/', views.ObtenerPeriodosPorAnioView.as_view(), name='api_periodos_por_anio'),
    path('api/materias-por-grado/<int:grado_id>/', views.ObtenerMateriasPorGradoView.as_view(), name='api_materias_por_grado'),

    # Grados
    path('grados/', ListaGradosView.as_view(), name='lista_grados'),
    path('grados/crear/', CrearGradoView.as_view(), name='crear_grado'),
    path('grados/editar/<int:pk>/', EditarGradoView.as_view(), name='editar_grado'),
    path('grados/eliminar/<int:pk>/', EliminarGradoView.as_view(), name='eliminar_grado'),
    
    # Materias
    path('materias/', views.ListaMateriasView.as_view(), name='lista_materias'),
    path('materias/crear/', views.CrearMateriaView.as_view(), name='crear_materia'),
    path('materias/<int:pk>/editar/', views.EditarMateriaView.as_view(), name='editar_materia'),
    path('materias/<int:pk>/eliminar/', views.EliminarMateriaView.as_view(), name='eliminar_materia'),

    # Notas
    path('notas/', views.lista_notas, name='lista_notas'),
    path('notas/crear/', views.crear_nota, name='crear_nota'),
    path('notas/<int:pk>/editar/', views.editar_nota, name='editar_nota'),
    path('notas/<int:pk>/eliminar/', views.eliminar_nota, name='eliminar_nota'),
    path('notas/importar/', views.importar_notas, name='importar_notas'),


    # Informes finales
    path('informes/', views.lista_informes_finales, name='lista_informes'),
    path('informes/crear/', views.crear_informe_final, name='crear_informe'),

]