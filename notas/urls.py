from django.urls import path
from . import views

app_name = 'notas'

urlpatterns = [

    #==========================0=========================QWEN==================================
    #==========================0=========================QWEN==================================

    path('escalas', views.EscalaNotaListView.as_view(), name='escala_lista'),
    path('nuevaescalas/crear/', views.EscalaNotaCreateView.as_view(), name='escala_nueva'),
    path('escalas/<int:pk>/editar/', views.EscalaNotaUpdateView.as_view(), name='escala_editar'),
    path('escalas/<int:pk>/eliminar/', views.EscalaNotaDeleteView.as_view(), name='escala_eliminar'),



    #==========================0=========================QWEN==================================
    #==========================0=========================QWEN==================================
    # Escalas de notas
    
    # path('escalas/', views.lista_escalas, name='lista_escalas'),
    # path('escalas/crear/', views.crear_escala, name='crear_escala'),
    #path('escalas/<int:pk>/editar/', views.editar_escala, name='editar_escala'),

    # Años escolares
    path('anios/crear/', views.AnioEscolarCreateView.as_view(), name='crear_anio'),
    path('anios/', views.gestionar_anios_periodos, name='lista_anios'),
    path('anios/<int:pk>/editar-estado/', views.editar_estado_anio, name='editar_estado_anio'),
    path('anios/<int:pk>/eliminar/', views.eliminar_anio_escolar, name='eliminar_anio'),


    # Grados
    path('grados/', views.lista_grados, name='lista_grados'),
    path('grados/crear/', views.crear_grado, name='crear_grado'),

    # Materias
    path('materias/', views.lista_materias, name='lista_materias'),
    path('materias/crear/', views.crear_materia, name='crear_materia'),
    path('materias/<int:pk>/editar/', views.editar_materia, name='editar_materia'),

    # Períodos
    path('periodos/', views.lista_periodos, name='lista_periodos'),
    path('periodos/crear/', views.crear_periodo, name='crear_periodo'),

    # Notas
    path('notas/', views.lista_notas, name='lista_notas'),
    path('notas/crear/', views.crear_nota, name='crear_nota'),
    path('notas/<int:pk>/editar/', views.editar_nota, name='editar_nota'),
    path('notas/<int:pk>/eliminar/', views.eliminar_nota, name='eliminar_nota'),
    path('notas/importar/', views.importar_notas, name='importar_notas'),


    # Informes finales
    path('informes/', views.lista_informes_finales, name='lista_informes'),
    path('informes/crear/', views.crear_informe_final, name='crear_informe'),

    # ===== NUEVAS RUTAS PARA GESTIÓN DE CURSOS DIRECTIVO =====
    # Gestión de cursos por directivo
    path('cursos-directivo/', views.cursos_directivo, name='cursos_directivo'),



]