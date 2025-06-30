from django import contrib
from django.contrib.auth import login
from django.urls import path
from .views import registro_usuario_general
from django.shortcuts import render
from django.contrib.auth import views as auth_views

#from users.views import CustomLoginView
#from users.views import RegisterView

urlpatterns = [
    path('login/',  contrib.auth.views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('registro/', registro_usuario_general, name='registro'),
    path('registro-exitoso/', lambda request: render(request, 'users/registro_exitoso.html'), name='registro_exitoso')
]