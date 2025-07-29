from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # 1. Define las opciones para el rol
    TIPO_USUARIO_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('profesor', 'Profesor'),
        ('directivo', 'Directivo'),
        ('acudiente', 'Acudiente'),
    ]

    # 2. Añade SOLO los campos nuevos que no existen en AbstractUser
    #    Nota: He renombrado 'role' a 'tipo_usuario' para que coincida con tus formularios.
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES, default='estudiante')
    documento = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=20, blank=True) # Usar CharField para teléfonos es más flexible
    direccion = models.CharField(max_length=200, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    nombre_colegio = models.CharField(max_length=100, blank=True)


    def __str__(self):
        return self.username


class Directivo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='directivo_profile')
    escuela = models.CharField(max_length=100)

    def __str__(self):
        return f"Directivo: {self.user.first_name} {self.user.last_name}"


class Profesor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profesor_profile')

    def __str__(self):
        return f"Profesor: {self.user.first_name} {self.user.last_name}"


class Estudiante(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='estudiante_profile')
    acudiente = models.ForeignKey('Acudiente', on_delete=models.SET_NULL, null=True, blank=True, related_name='estudiantes')
    profesor = models.ForeignKey('Profesor', on_delete=models.SET_NULL, null=True, blank=True, related_name='estudiantes')

    def __str__(self):
        return f"Estudiante: {self.user.first_name} {self.user.last_name}"


class Acudiente(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='acudiente_profile')

    def __str__(self):
        return f"Acudiente: {self.user.first_name} {self.user.last_name}"
