from django.urls import path
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from .views import registro_view


urlpatterns = [
    path('registro/', registro_view, name='registro'),
    path('login/', LoginView.as_view(template_name="users/login.html"), name="login"),
path('logout/', LogoutView.as_view(next_page='login'), name="logout"),
    path('dashboard/', lambda request: render(request, 'users/dashboard.html'), name='dashboard'),

    path('registro-exitoso/', lambda request: render(request, 'users/registro_exitoso.html'), name='registro_exitoso'),
]
