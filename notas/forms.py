from django import forms
from django.core.exceptions import ValidationError
from .models import EscalaNota, AnioEscolar, Grado, Materia, Periodo, Nota, InformeFinal
from users.models import Profesor, Estudiante


class EscalaNotaForm(forms.ModelForm):
    class Meta:
        model = EscalaNota
        fields = ['nombre', 'minimo', 'maximo', 'paso']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Escala 0 a 5'
            }),
            'minimo': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'maximo': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'paso': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        minimo = cleaned_data.get('minimo')
        maximo = cleaned_data.get('maximo')
        
        if minimo and maximo and minimo >= maximo:
            raise ValidationError('El valor mínimo debe ser menor que el máximo.')
        
        return cleaned_data


class AnioEscolarForm(forms.ModelForm):
    class Meta:
        model = AnioEscolar
        fields = ['anio', 'activo', 'escala']
        widgets = {
            'anio': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '2020',
                'max': '2030'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'escala': forms.Select(attrs={
                'class': 'form-select'
            })
        }


class GradoForm(forms.ModelForm):
    class Meta:
        model = Grado
        fields = ['nombre', 'anio']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Grado 11°'
            }),
            'anio': forms.Select(attrs={
                'class': 'form-select'
            })
        }


class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = ['nombre', 'grado', 'profesor']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Matemáticas'
            }),
            'grado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'profesor': forms.Select(attrs={
                'class': 'form-select'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar profesores activos
        self.fields['profesor'].queryset = Profesor.objects.filter(user__is_active=True)


class PeriodoForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = ['anio_escolar', 'nombre', 'porcentaje']
        widgets = {
            'anio_escolar': forms.Select(attrs={
                'class': 'form-select'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Primer Período'
            }),
            'porcentaje': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100'
            })
        }

    def clean_porcentaje(self):
        porcentaje = self.cleaned_data.get('porcentaje')
        if porcentaje and (porcentaje < 0 or porcentaje > 100):
            raise ValidationError('El porcentaje debe estar entre 0 y 100.')
        return porcentaje


class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['estudiante', 'materia', 'periodo', 'descripcion', 'valor', 'porcentaje']
        widgets = {
            'estudiante': forms.Select(attrs={
                'class': 'form-select'
            }),
            'materia': forms.Select(attrs={
                'class': 'form-select'
            }),
            'periodo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Examen parcial'
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'porcentaje': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar estudiantes activos
        self.fields['estudiante'].queryset = Estudiante.objects.filter(user__is_active=True)

    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        periodo = self.cleaned_data.get('periodo')
        
        if valor and periodo:
            escala = periodo.anio_escolar.escala
            if not (escala.minimo <= valor <= escala.maximo):
                raise ValidationError(
                    f'La nota debe estar entre {escala.minimo} y {escala.maximo} '
                    f'(escala: {escala.nombre}).'
                )
        return valor

    def clean_porcentaje(self):
        porcentaje = self.cleaned_data.get('porcentaje')
        if porcentaje and (porcentaje < 0 or porcentaje > 100):
            raise ValidationError('El porcentaje debe estar entre 0 y 100.')
        return porcentaje


class InformeFinalForm(forms.ModelForm):
    class Meta:
        model = InformeFinal
        fields = ['estudiante', 'materia', 'anio_escolar', 'promedio_final']
        widgets = {
            'estudiante': forms.Select(attrs={
                'class': 'form-select'
            }),
            'materia': forms.Select(attrs={
                'class': 'form-select'
            }),
            'anio_escolar': forms.Select(attrs={
                'class': 'form-select'
            }),
            'promedio_final': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar estudiantes activos
        self.fields['estudiante'].queryset = Estudiante.objects.filter(user__is_active=True)


# Formularios para búsqueda y filtros
class BuscarEstudianteForm(forms.Form):
    nombre = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre...'
        })
    )
    grado = forms.ModelChoiceField(
        queryset=Grado.objects.all(),
        required=False,
        empty_label="Todos los grados",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )


class BuscarNotaForm(forms.Form):
    estudiante = forms.ModelChoiceField(
        queryset=Estudiante.objects.filter(user__is_active=True),
        required=False,
        empty_label="Todos los estudiantes",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    materia = forms.ModelChoiceField(
        queryset=Materia.objects.all(),
        required=False,
        empty_label="Todas las materias",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    periodo = forms.ModelChoiceField(
        queryset=Periodo.objects.all(),
        required=False,
        empty_label="Todos los períodos",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )


# Formulario para importar notas masivamente
class ImportarNotasForm(forms.Form):
    archivo = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xls,.csv'
        })
    )
    periodo = forms.ModelChoiceField(
        queryset=Periodo.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    materia = forms.ModelChoiceField(
        queryset=Materia.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        if archivo:
            # Validar extensión del archivo
            extension = archivo.name.split('.')[-1].lower()
            if extension not in ['xlsx', 'xls', 'csv']:
                raise ValidationError('El archivo debe ser Excel (.xlsx, .xls) o CSV.')
        return archivo
