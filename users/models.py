from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Añade campos personalizados aquí si es necesario
    pass

class Profesor(models.Model):
    docu_profesor = models.IntegerField()
    profe_especialidad = models.CharField(max_length=45, blank=True, null=True)
    profe_email = models.CharField(max_length=45, blank=True, null=True)
    profe_nombre = models.CharField(max_length=45, blank=True, null=True)
    profe_apellido = models.CharField(max_length=45, blank=True, null=True)
    profe_escalafon = models.CharField(max_length=45, blank=True, null=True)
    profe_area = models.CharField(max_length=45, blank=True, null=True)
    profe_tel = models.IntegerField()

    def __str__(self):
        return f"Profesor: {self.profe_nombre} {self.profe_apellido}"


class Estudiante(models.Model):
    docu_estudiante = models.IntegerField()
    estu_nombre = models.CharField(max_length=45, blank=True, null=True)
    estu_apellido = models.CharField(max_length=45, blank=True, null=True)
    estu_email = models.CharField(max_length=45, blank=True, null=True)
    estu_tel = models.IntegerField()
    profesor_docu_profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE) # Foreign key to Profesor
    acudiente_docu_acudiente = models.ForeignKey('Acudiente', on_delete=models.CASCADE)  # Foreign key to Acudiente

    def __str__(self):
        return f"Estudiante: {self.estu_nombre} {self.estu_apellido}"

from django.db import models

class Acudiente(models.Model):
    docu_acudiente = models.IntegerField()
    acu_nombre = models.CharField(max_length=45, blank=True, null=True)
    acu_apellido = models.CharField(max_length=45, blank=True, null=True)
    acu_email = models.CharField(max_length=45, blank=True, null=True)
    acu_tel = models.IntegerField()

    def __str__(self):
        return f"Acudiente: {self.acu_nombre} {self.acu_apellido}"



