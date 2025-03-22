from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('estudiante', 'Estudiante'),
        ('profesor', 'Profesor'),
        ('administracion', 'Administración'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='estudiante')

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
