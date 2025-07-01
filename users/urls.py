# users/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import registro_usuario_general

urlpatterns = [
    path('registro/', registro_usuario_general, name='registro'),
    path('login/', LoginView.as_view(template_name="users/login.html"), name="login"),
    path('logout/', LogoutView.as_view(next_page='login'), name="logout"),
    path('registro-exitoso/', lambda request: render(request, 'users/registro_exitoso.html'), name='registro_exitoso'),
]
