from django.urls import path
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from .views import registro_view, registro_exitoso_view, CustomLoginView
from .views import dashboard_estudiante, cursos_estudiante, notas_estudiante, boletin_estudiante, tareas_estudiante, perfil_estudiante
from .views import dashboard_profesor


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


]