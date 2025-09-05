from django.urls import path
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from .views import registro_view, registro_exitoso_view, CustomLoginView
from .views import dashboard_estudiante, cursos_estudiante, notas_estudiante, boletin_estudiante, tareas_estudiante, perfil_estudiante
from .views import dashboard_profesor, cursos_profesor, calificaciones_profesor, estudiantes_profesor, tareas_profesor, perfil_profesor
from .views import dashboard_directivo, usuarios_directivo, cursos_directivo, horarios_directivo, reportes_directivo, perfil_directivo
from .views import dashboard_acudiente, perfil_acudiente, estudiantes_acudiente, notas_acudiente, boletin_acudiente, tareas_acudiente


urlpatterns = [
    path('registro/', registro_view, name='registro'),
    path('login/', CustomLoginView.as_view(template_name="users/login.html"), name="login"),
    path('logout/', LogoutView.as_view(next_page="landing"), name="logout"),


    path('registro-exitoso/', registro_exitoso_view, name='registro_exitoso'),

# Estudiante ----------------------------------------------
    path('estudiante/dashboard/', dashboard_estudiante, name='dashboard_estudiante'),
    path('estudiante/cursos/', cursos_estudiante,  name='cursos_estudiante'),
    path('estudiante/notas/', notas_estudiante, name='notas_estudiante'),
    path('estudiante/boletin/', boletin_estudiante, name='boletin_estudiante'),
    path('estudiante/tareas/', tareas_estudiante, name='tareas_estudiante'),
    path('estudiante/perfil/', perfil_estudiante, name='perfil_estudiante'),

# Profesor
    path('profesor/dashboard/', dashboard_profesor, name='dashboard_profesor'),
    path('profesor/cursos/', cursos_profesor, name='cursos_profesor'),
    path('profesor/calificaciones/', calificaciones_profesor, name='calificaciones_profesor'),
    path('profesor/estudiantes/', estudiantes_profesor, name='estudiantes_profesor'),
    path('profesor/tareas/', tareas_profesor, name='tareas_profesor'),
    path('profesor/perfil/', perfil_profesor, name='perfil_profesor'),
    
# Directivo
    path('directivo/dashboard/', dashboard_directivo, name='dashboard_directivo'),
    path('directivo/usuarios/', usuarios_directivo, name='usuarios_directivo'),
    path('directivo/cursos/', cursos_directivo, name='cursos_directivo'),
    path('directivo/horarios/', horarios_directivo, name='horarios_directivo'),
    path('directivo/reportes/', reportes_directivo, name='reportes_directivo'),
    path('directivo/perfil/', perfil_directivo, name='perfil_directivo'),
    
# Acudiente
    path('acudiente/dashboard/', dashboard_acudiente, name='dashboard_acudiente'),
    path('acudiente/perfil/', perfil_acudiente, name='perfil_acudiente'),
    path('acudiente/estudiantes/', estudiantes_acudiente, name='estudiantes_acudiente'),
    path('acudiente/notas/', notas_acudiente, name='notas_acudiente'),
    path('acudiente/boletin/', boletin_acudiente, name='boletin_acudiente'),
    path('acudiente/tareas/', tareas_acudiente, name='tareas_acudiente'),

]