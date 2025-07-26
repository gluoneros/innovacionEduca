from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('profesor', 'Profesor'),
        ('directivo', 'Directivo'),
        ('acudiente', 'Acudiente'),
    ]
    role = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES)
    documento = models.CharField(max_length=100, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    nombre = models.CharField(max_length=100, blank=True)
    apellido = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)

class Directivo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='Directivo')
    escuela = models.CharField(max_length=100)

    def __str__(self):
        return f"Directivo: {self.user.nombre} {self.user.apellido}"

class Profesor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='Profesor')

    def __str__(self):
        return f"Profesor: {self.user.nombre} {self.user.apellido}"


class Estudiante(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='Estudiante')

    profesor_docu_profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE) # Foreign key to Profesor
    acudiente_docu_acudiente = models.ForeignKey('Acudiente', on_delete=models.CASCADE)  # Foreign key to Acudiente

    acudiente_docu_acudiente = models.ForeignKey('Acudiente', on_delete=models.SET_NULL, null=True, blank=True)
    profesor_docu_profesor = models.ForeignKey('Profesor', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Estudiante: {self.user.nombre} {self.user.apellido}"



class Acudiente(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='Acudiente')

    def __str__(self):
        return f"Acudiente: {self.acu_nombre} {self.acu_apellido}"



