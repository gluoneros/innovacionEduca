from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegistroGeneralForm
from django.contrib.auth import login
import random

def generar_id():
    return random.randint(100000, 999999)


def registro_view(request):
    if request.method == 'POST':
        form = RegistroGeneralForm(request.POST)
        if form.is_valid():
            user = form.save()  # El metodo .save() ahora crea y guarda el usuario!
            login(request, user)  # Inicia sesión automáticamente al nuevo usuario
            return redirect('registro_exitoso')  # O a la página que quieras
    else:
        form = RegistroGeneralForm()

    return render(request, 'users/register.html', {'form': form})

def registro_exitoso_view(request):
    context = {
        'user': request.user
    }
    return render(request, 'users/registro_exitoso.html', context)

@login_required # Este decorador protege la vista, solo usuarios logueados pueden entrar.
def dashboard_view(request):
    """
    Muestra el panel de control del usuario que ha iniciado sesión.
    """
    # El objeto 'request.user' contiene toda la información del usuario logueado.
    # Lo pasamos a la plantilla a través del diccionario de contexto.
    context = {
        'user': request.user
    }
    return render(request, 'users/dashboard_base.html', context)




@login_required
def dashboard(request):
    return render(request, 'users/dashboard_base.html', {'user': request.user})