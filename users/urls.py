from django.urls import path
from .views import registro_usuario_general
from django.shortcuts import render

#from users.views import CustomLoginView
#from users.views import RegisterView

urlpatterns = [
    path('registro/', registro_usuario_general, name='registro'),
    path('registro-exitoso/', lambda request: render(request, 'users/registro_exitoso.html'), name='registro_exitoso')
]