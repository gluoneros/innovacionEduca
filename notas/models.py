from django.db import models
from users.models import Profesor, Estudiante


class Grado(models.Model):
    nombre = models.CharField(max_length=100)
    estudiantes = models.ManyToManyField(Estudiante, related_name='grados')
    profesores = models.ManyToManyField(Profesor, related_name='grados')
    materias = models.ManyToManyField('Materia', related_name='grados')
    
    def __str__(self):
        return self.nombre

class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name='materias')
    estudiantes = models.ManyToManyField(Estudiante, related_name='materias')
    grados = models.ManyToManyField(Grado, related_name='materias')
    notas = models.ManyToManyField('Nota', related_name='materias')
    
    def __str__(self):
        return self.nombre
    
class Nota(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='notas')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='notas')
    nota = models.FloatField()
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.estudiante.user.first_name} {self.estudiante.user.last_name} - {self.materia.nombre} - {self.nota}"