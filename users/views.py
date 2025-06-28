from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

class RegisterView(generic.CreateView):
    form_class = CustomUserCreationForm  # Usa el formulario personalizado
    template_name = "users/register.html"
    success_url = reverse_lazy("login")

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirige o muestra mensaje de éxito
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})