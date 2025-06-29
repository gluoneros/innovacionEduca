'''from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'tipo_usuario', 'password1', 'password2')
'''
from django import forms
from .models import Estudiante, Profesor, Acudiente, directivo
# users/forms.py


class RegistroGeneralForm(forms.Form):
    TIPO_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('profesor', 'Profesor'),
        ('acudiente', 'Acudiente'),
        ('directivo', 'Directivo'),
    ]

    nombre = forms.CharField(max_length=45)
    apellido = forms.CharField(max_length=45)
    email = forms.EmailField()
    telefono = forms.IntegerField()
    tipo_usuario = forms.ChoiceField(choices=TIPO_CHOICES)
