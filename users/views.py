from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
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

class CustomLoginView(LoginView):
    template_name = "users/login.html"

    def get_success_url(self):
        user = self.request.user
        if user.tipo_usuario == "estudiante":
            return reverse_lazy("dashboard_estudiante")
        elif user.tipo_usuario == "profesor":
            return reverse_lazy("dashboard_profesor")
        elif user.tipo_usuario == "directivo":
            return reverse_lazy("dashboard_directivo")
        elif user.tipo_usuario == "acudiente":
            return reverse_lazy("dashboard_acudiente")
        return reverse_lazy("dashboard")

#estudiantes----------------------------------------------
@login_required
def dashboard_estudiante(request):
    return render(request, 'users/estudiante/dashboard_estudiante.html')

@login_required
def cursos_estudiante(request):
    return render(request, 'users/estudiante/cursos_estudiante.html')

@login_required
def notas_estudiante(request):
    return render(request, 'users/estudiante/notas_estudiante.html')

@login_required
def boletin_estudiante(request):
    return render(request, 'users/estudiante/boletin_estudiante.html')

@login_required
def tareas_estudiante(request):
    return render(request, 'users/estudiante/tareas_estudiante.html')

@login_required
def perfil_estudiante(request):
    return render(request, 'users/estudiante/perfil_estudiante.html')

#profesor----------------------------------------------
@login_required
def dashboard_profesor(request):
    tipo = request.user.tipo_usuario # selecciona el contenido segun el tipo de usuario

    template_map = {
        'estudiante': 'users/estudiante/dashboard_estudiante.html',
        'profesor': 'users/profesor/dashboard_profesor.html',
        'directivo': 'users/directivo/dashboard_directivo.html',
        'acudiente': 'users/acudiente/dashboard_acudiente.html',
    }


    return render(request, template_map.get(tipo, 'users/profesor/dashboard_profesor.html'), {
        'user': request.user
    })
