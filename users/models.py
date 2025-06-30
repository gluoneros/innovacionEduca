from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('profesor', 'Profesor'),
        ('directivo', 'Directivo'),
        ('acudiente', 'Acudiente'),
    ]
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES, default='estudiante')

class directivo(models.Model):
    docu_directivo = models.BigIntegerField()
    dire_nombre = models.CharField(max_length=45, blank=True, null=True)
    dire_apellido = models.CharField(max_length=45, blank=True, null=True)
    dire_email = models.CharField(max_length=45, blank=True, null=True)
    dire_tel = models.BigIntegerField()

    def __str__(self):
        return f"Directivo: {self.dire_nombre} {self.dire_apellido}"

class Profesor(models.Model):
    docu_profesor = models.BigIntegerField()
    profe_especialidad = models.CharField(max_length=45, blank=True, null=True)
    profe_email = models.CharField(max_length=45, blank=True, null=True)
    profe_nombre = models.CharField(max_length=45, blank=True, null=True)
    profe_apellido = models.CharField(max_length=45, blank=True, null=True)
    profe_escalafon = models.CharField(max_length=45, blank=True, null=True)
    profe_area = models.CharField(max_length=45, blank=True, null=True)
    profe_tel = models.BigIntegerField()

    def __str__(self):
        return f"Profesor: {self.profe_nombre} {self.profe_apellido}"


class Estudiante(models.Model):
    docu_estudiante = models.BigIntegerField()
    estu_nombre = models.CharField(max_length=45, blank=True, null=True)
    estu_apellido = models.CharField(max_length=45, blank=True, null=True)
    estu_email = models.CharField(max_length=45, blank=True, null=True)
    estu_tel = models.BigIntegerField()
    profesor_docu_profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE) # Foreign key to Profesor
    acudiente_docu_acudiente = models.ForeignKey('Acudiente', on_delete=models.CASCADE)  # Foreign key to Acudiente

    acudiente_docu_acudiente = models.ForeignKey('Acudiente', on_delete=models.SET_NULL, null=True, blank=True)
    profesor_docu_profesor = models.ForeignKey('Profesor', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Estudiante: {self.estu_nombre} {self.estu_apellido}"



class Acudiente(models.Model):
    docu_acudiente = models.BigIntegerField()
    acu_nombre = models.CharField(max_length=45, blank=True, null=True)
    acu_apellido = models.CharField(max_length=45, blank=True, null=True)
    acu_email = models.CharField(max_length=45, blank=True, null=True)
    acu_tel = models.BigIntegerField()



    def __str__(self):
        return f"Acudiente: {self.acu_nombre} {self.acu_apellido}"



