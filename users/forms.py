from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profesor, Estudiante, Directivo, Acudiente


class RegistroGeneralForm(UserCreationForm):
    """
    Un ModelForm para crear un nuevo usuario y su perfil asociado.
    """
    # Para el campo de fecha, es mejor definirlo explícitamente
    # para poder usar un widget de tipo 'date'.
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        label="Fecha de Nacimiento"
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # --- ¡AQUÍ ESTÁ EL CAMBIO PRINCIPAL! ---
        # Añadimos los nuevos campos a la lista.
        fields = ('username', 'first_name', 'last_name', 'email', 'telefono',
                    'tipo_usuario', 'fecha_nacimiento', 'nombre_colegio')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Tu código para los estilos es perfecto.
        # Solo nos aseguramos de que los labels estén correctos.
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellido"
        self.fields['nombre_colegio'].label = "Nombre del Colegio"
        self.fields['tipo_usuario'].label = "Tipo de Usuario"

        for field_name, field in self.fields.items():
            # Aplicamos los placeholders y clases
            placeholder_text = field.label
            if hasattr(placeholder_text, 'lower'):
                placeholder_text = f'Ingresa tu {placeholder_text.lower()}'

            field.widget.attrs.update({
                'class': 'form-input w-full pl-12',
                'placeholder': placeholder_text
            })
            if field_name == 'email':
                field.widget.attrs['placeholder'] = 'ejemplo@correo.com'
            if field_name == 'tipo_usuario':
                field.widget.attrs.update({
                    'class': 'form-input w-full pl-12 appearance-none'
                })
            # El widget de fecha ya tiene su tipo definido, no necesita placeholder.
            if field_name == 'fecha_nacimiento':
                field.widget.attrs.pop('placeholder', None)

    def save(self, commit=True):
        """
        Sobrescribimos el metodo save para crear el usuario, guardar los
        campos adicionales y finalmente crear el perfil.
        """
        # 1. Usamos commit=False para obtener el objeto user sin guardarlo aún.
        user = super().save(commit=False)

        # 2. Añadimos los datos de los nuevos campos al objeto user.
        user.fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        user.nombre_colegio = self.cleaned_data.get('nombre_colegio')

        # 3. Ahora sí, guardamos el objeto user con todos sus datos.
        if commit:
            user.save()

        # 4. Lee el tipo de usuario para crear el perfil asociado.
        tipo_usuario = self.cleaned_data.get('tipo_usuario')
        if tipo_usuario == 'profesor':
            Profesor.objects.create(user=user)
        elif tipo_usuario == 'estudiante':
            Estudiante.objects.create(user=user)
        elif tipo_usuario == 'directivo':
            # Usamos el nombre del colegio del formulario.
            Directivo.objects.create(user=user, escuela=user.nombre_colegio)
        elif tipo_usuario == 'acudiente':
            Acudiente.objects.create(user=user)

        return user