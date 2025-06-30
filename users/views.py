# users/views.py
from django.shortcuts import render, redirect
from .forms import RegistroGeneralForm
from .models import Estudiante, Profesor, Acudiente, directivo
import random

def generar_id():
    return random.randint(100000, 999999)

def registro_usuario_general(request):
    if request.method == 'POST':
        form = RegistroGeneralForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            email = form.cleaned_data['email']
            telefono = form.cleaned_data['telefono']
            tipo = form.cleaned_data['tipo_usuario']

            if tipo == 'estudiante':
                Estudiante.objects.create(
                    docu_estudiante=generar_id(),
                    estu_nombre=nombre,
                    estu_apellido=apellido,
                    estu_email=email,
                    estu_tel=telefono,
                    profesor_docu_profesor_id=1,  # dummy
                    acudiente_docu_acudiente_id=1  # dummy
                )
            elif tipo == 'profesor':
                Profesor.objects.create(
                    docu_profesor=generar_id(),
                    profe_nombre=nombre,
                    profe_apellido=apellido,
                    profe_email=email,
                    profe_tel=telefono
                )
            elif tipo == 'acudiente':
                Acudiente.objects.create(
                    docu_acudiente=generar_id(),
                    acu_nombre=nombre,
                    acu_apellido=apellido,
                    acu_email=email,
                    acu_tel=telefono
                )
            elif tipo == 'directivo':
                directivo.objects.create(
                    docu_directivo=generar_id(),
                    dire_nombre=nombre,
                    dire_apellido=apellido,
                    dire_email=email,
                    dire_tel=telefono
                )

            return redirect('registro_exitoso')  # asegúrate de tener esta URL
    else:
        form = RegistroGeneralForm()

    return render(request, 'users/register.html', {'form': form})
