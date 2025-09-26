from django.urls import path
from . import views

app_name = 'notas'

urlpatterns = [
    # Escalas de notas
    path('escalas/', views.lista_escalas, name='lista_escalas'),
    path('escalas/crear/', views.crear_escala, name='crear_escala'),
    path('escalas/<int:pk>/editar/', views.editar_escala, name='editar_escala'),

    # Años escolares
    path('anios/', views.lista_anios_escolares, name='lista_anios'),
    path('anios/crear/', views.crear_anio_escolar, name='crear_anio'),

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

    # AJAX endpoints
    path('ajax/crear-anio/', views.crear_anio_escolar_ajax, name='crear_anio_ajax'),
    path('ajax/crear-grado/', views.crear_grado_ajax, name='crear_grado_ajax'),
    path('ajax/crear-materia/', views.crear_materia_ajax, name='crear_materia_ajax'),
    path('ajax/crear-escala/', views.crear_escala_ajax, name='crear_escala_ajax'),
    path('ajax/obtener-datos-anio/<int:anio_id>/', views.obtener_datos_anio, name='obtener_datos_anio'),
    path('ajax/editar-materia/<int:materia_id>/', views.editar_materia_ajax, name='editar_materia_ajax'),
    path('ajax/eliminar-materia/<int:materia_id>/', views.eliminar_materia_ajax, name='eliminar_materia_ajax'),
    path('ajax/obtener-materia/<int:materia_id>/', views.obtener_materia_ajax, name='obtener_materia_ajax'),
    path('ajax/activar-anio/<int:anio_id>/', views.activar_anio_escolar, name='activar_anio'),
    path('ajax/crear-periodo/', views.crear_periodo_ajax, name='crear_periodo_ajax'),
    path('ajax/estadisticas-anio/<int:anio_id>/', views.obtener_estadisticas_anio, name='estadisticas_anio'),
]