from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('hola/', views.hola_mundo, name='hola_mundo'),
]
