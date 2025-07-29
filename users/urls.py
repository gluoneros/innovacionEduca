from django.urls import path
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from .views import registro_view, dashboard_view, registro_exitoso_view 


urlpatterns = [
    path('registro/', registro_view, name='registro'),
    path('login/', LoginView.as_view(template_name="users/login.html"), name="login"),
    path('logout/', LogoutView.as_view(next_page='login'), name="logout"),

    # Reemplazamos la lambda con nuestra nueva vista
    path('dashboard/', dashboard_view, name='dashboard'),

    path('registro-exitoso/', registro_exitoso_view, name='registro_exitoso'),
]