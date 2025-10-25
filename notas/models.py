from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum, F

from users.models import Profesor, Estudiante

ESCALAS_PREDEFINIDAS = [
    ("0 a 5", 0.00, 5.00),
    ("1 a 5", 1.00, 5.00),
    ("0 a 10", 0.00, 10.00),
    ("1 a 10", 1.00, 10.00),
]

class EscalaNota(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    minimo = models.DecimalField(max_digits=5, decimal_places=2)  # aumenté a 5 para soportar 10.00
    maximo = models.DecimalField(max_digits=5, decimal_places=2)
    paso = models.DecimalField(max_digits=4, decimal_places=2, default=0.01)

    def __str__(self):
        return f"{self.nombre} ({self.minimo} - {self.maximo})"


# Entidad que representa el año escolars
class AnioEscolar(models.Model):
    anio = models.PositiveIntegerField(unique=True)
    activo = models.BooleanField(default=True)
    escala = models.ForeignKey(EscalaNota, on_delete=models.PROTECT, related_name="anios_escolares")

    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Validación: Solo puede haber un año activo a la vez
        if self.activo:
            anio_activo_existente = AnioEscolar.objects.filter(activo=True).exclude(pk=self.pk).first()
            
            if anio_activo_existente:
                raise ValidationError(
                    f'No se puede activar el año {self.anio} porque ya existe el año {anio_activo_existente.anio} activo. '
                    f'Solo puede haber un año escolar activo a la vez.'
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.anio)   

class Periodo(models.Model):
    anio_escolar = models.ForeignKey(AnioEscolar, on_delete=models.CASCADE, related_name='periodos')
    nombre = models.CharField(max_length=50)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)

    # Calcula el promedio de un estudiante en este periodo
    # considerando las notas y sus porcentajes
    # Retorna None si no hay notas
    def promedio_estudiante(self, estudiante):
        notas = self.notas.filter(estudiante=estudiante)
        if not notas.exists():
            return None
        total = notas.aggregate(suma=Sum(F('valor') * F('porcentaje') / 100))['suma']

        return round(total, 2) if total is not None else None

    # Valida que la suma de los porcentajes no supere 100%
    def clean(self):
        super().clean()
        total = Periodo.objects.filter(anio_escolar=self.anio_escolar) \
                    .exclude(pk=self.pk) \
                    .aggregate(suma=Sum("porcentaje"))["suma"] or 0
        if total + self.porcentaje > 100:
            raise ValidationError("La suma de los porcentajes de los periodos no puede superar 100%.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ("anio_escolar", "nombre")
    
    def __str__(self):
        return f"{self.anio_escolar.anio} - {self.nombre}"


class Grado(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    anio = models.ForeignKey(AnioEscolar, on_delete=models.SET_NULL, null=True, blank=True, related_name='grados')

    def __str__(self):
        return self.nombre


# Entidad que representa la materia
class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    grado = models.ForeignKey(Grado, on_delete=models.SET_NULL, null=True, blank=True, related_name='materias')
    profesor = models.ForeignKey(Profesor, on_delete=models.SET_NULL, null=True, blank=True)

    # Evita duplicados por grado
    class Meta:
        unique_together = ("nombre", "grado")

    def __str__(self):
        return self.nombre

class Nota(models.Model):
    estudiante = models.ForeignKey("users.Estudiante", on_delete=models.CASCADE, related_name="notas")
    materia = models.ForeignKey("Materia", on_delete=models.CASCADE, related_name="notas")
    periodo = models.ForeignKey("Periodo", on_delete=models.CASCADE, related_name="notas")
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    valor = models.DecimalField(max_digits=5, decimal_places=2)  
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)

    def clean(self):
        # Accedemos a la escala a través del periodo -> año escolar -> escala
        escala = self.periodo.anio_escolar.escala
        if not (escala.minimo <= self.valor <= escala.maximo):
            raise ValidationError(
                f"La nota debe estar entre {escala.minimo} y {escala.maximo} "
                f"(escala: {escala.nombre})."
            )
    
    class Meta:
        unique_together = ("estudiante", "materia", "periodo", "descripcion")


    def __str__(self):
        return f"{self.estudiante} - {self.materia} - {self.periodo} : {self.valor}"
    
class InformeFinal(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="informes_finales")
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name="informes_finales")
    anio_escolar = models.ForeignKey(AnioEscolar, on_delete=models.CASCADE)
    promedio_final = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ("estudiante", "materia", "anio_escolar")

    def __str__(self):
        return f"Informe {self.estudiante} - {self.materia} ({self.anio_escolar.anio})"