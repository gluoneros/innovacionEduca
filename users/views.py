from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .forms import RegistroGeneralForm
from django.contrib.auth import login
import random
from notas.models import AnioEscolar

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

@login_required
def dashboard(request):
    """Vista de dashboard genérico que redirige según el tipo de usuario"""
    user = request.user
    if user.tipo_usuario == "estudiante":
        return redirect("dashboard_estudiante")
    elif user.tipo_usuario == "profesor":
        return redirect("dashboard_profesor")
    elif user.tipo_usuario == "directivo":
        return redirect("dashboard_directivo")
    elif user.tipo_usuario == "acudiente":
        return redirect("dashboard_acudiente")
    # Si no tiene tipo de usuario definido, redirigir al login
    return redirect("login")

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
    return render(request, 'users/profesor/dashboard_profesor.html')

@login_required
def cursos_profesor(request):
    return render(request, 'users/profesor/cursos_profesor.html')

@login_required
def calificaciones_profesor(request):
    return render(request, 'users/profesor/calificaciones_profesor.html')

@login_required
def estudiantes_profesor(request):
    return render(request, 'users/profesor/estudiantes_profesor.html')

@login_required
def tareas_profesor(request):
    return render(request, 'users/profesor/tareas_profesor.html')

@login_required
def perfil_profesor(request):
    return render(request, 'users/profesor/perfil_profesor.html')


#directivo----------------------------------------------
@login_required
def dashboard_directivo(request):
    return render(request, 'users/directivo/dashboard_directivo.html')

@login_required
def usuarios_directivo(request):
    return render(request, 'users/directivo/usuarios_directivo.html')

@login_required
def cursos_directivo(request):
    anios = AnioEscolar.objects.select_related('escala').prefetch_related('periodos').order_by('-anio')
    return render(request, 'users/directivo/cursos_directivo.html', {'anios': anios})

@login_required
def horarios_directivo(request):
    return render(request, 'users/directivo/horarios_directivo.html')

@login_required
def reportes_directivo(request):
    return render(request, 'users/directivo/reportes_directivo.html')

@login_required
def perfil_directivo(request):
    return render(request, 'users/directivo/perfil_directivo.html')

#acudiente----------------------------------------------
@login_required
def dashboard_acudiente(request):
    return render(request, 'users/acudiente/dashboard_acudiente.html')

@login_required
def perfil_acudiente(request):
    return render(request, 'users/acudiente/perfil_acudiente.html')

@login_required
def estudiantes_acudiente(request):
    return render(request, 'users/acudiente/estudiantes_acudiente.html')

@login_required
def notas_acudiente(request):
    return render(request, 'users/acudiente/notas_acudiente.html')

@login_required
def boletin_acudiente(request):
    return render(request, 'users/acudiente/boletin_acudiente.html')

@login_required
def tareas_acudiente(request):
    return render(request, 'users/acudiente/tareas_acudiente.html')
