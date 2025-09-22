"""
URL configuration for innovacioneducativa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls), # Habilitar el admin general, util a veces
    path('', include('core.urls')),  # Incluye las URLs de la aplicación core
    
    path('usuarios/', include('users.urls')), # Urls de la app users
    path('', RedirectView.as_view(url='/usuarios/login/', permanent=False)),  # Redirige la raíz al login
    
    path('notas/', include('notas.urls')), # Urls de la app notas

]

# Handlers de errores
handler404 = 'core.views.page_not_found'