'''from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'tipo_usuario', 'password1', 'password2')
'''
# forms.py
from django import forms

TIPOS_USUARIO = [
    ('estudiante', 'Estudiante'),
    ('profesor', 'Profesor'),
    ('acudiente', 'Acudiente'),
    ('directivo', 'Directivo'),
]

class RegistroGeneralForm(forms.Form):
    nombre = forms.CharField(label='Nombre')
    apellido = forms.CharField(label='Apellido')
    email = forms.EmailField(label='Correo electrónico')
    telefono = forms.IntegerField(label='Teléfono')
    tipo_usuario = forms.ChoiceField(choices=TIPOS_USUARIO, label='Tipo de usuario')
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({
            'class': 'w-full rounded border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })