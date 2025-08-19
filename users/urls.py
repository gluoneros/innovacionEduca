from django.urls import path
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from .views import registro_view, dashboard_view, registro_exitoso_view, CustomLoginView
from .views import dashboard_estudiante, cursos_estudiante, notas_estudiante, boletin_estudiante, tareas_estudiante, perfil_estudiante


urlpatterns = [
    path('registro/', registro_view, name='registro'),
    path('login/', CustomLoginView.as_view(template_name="users/login.html"), name="login"),
    path('logout/', LogoutView.as_view(next_page="landing"), name="logout"),

    # Reemplazamos la lambda con nuestra nueva vista
    path('dashboard/', dashboard_view, name='dashboard'),

    path('registro-exitoso/', registro_exitoso_view, name='registro_exitoso'),

# Estudiante
    path('estudiante/dashboard/', dashboard_estudiante, name='dashboard_estudiante'),
    path('estudiante/cursos/', cursos_estudiante,  name='cursos_estudiante'),
    path('estudiante/notas/', notas_estudiante, name='notas_estudiante'),
    path('estudiante/boletin/', boletin_estudiante, name='boletin_estudiante'),
    path('estudiante/tareas/', tareas_estudiante, name='tareas_estudiante'),
    path('estudiante/perfil/', perfil_estudiante, name='perfil_estudiante'),


]