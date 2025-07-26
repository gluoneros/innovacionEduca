# users/views.py
from django.shortcuts import render, redirect
from .forms import RegistroGeneralForm
from .models import Estudiante, Profesor, Acudiente, Directivo, CustomUser
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

            # Crear usuario base
            user = CustomUser.objects.create(
                username=f"{nombre.lower()}.{apellido.lower()}{generar_id()}",
                nombre=nombre,
                apellido=apellido,
                email=email,
                tel=telefono,
                role=tipo
            )

            if tipo == 'estudiante':
                Estudiante.objects.create(
                    user=user,
                    # Asigna profesor y acudiente válidos aquí
                )
            elif tipo == 'profesor':
                Profesor.objects.create(user=user)
            elif tipo == 'acudiente':
                Acudiente.objects.create(user=user)
            elif tipo == 'directivo':
                Directivo.objects.create(user=user, escuela="")  # Ajusta escuela según el formulario

            return redirect('registro_exitoso')
    else:
        form = RegistroGeneralForm()

    return render(request, 'users/register.html', {'form': form})