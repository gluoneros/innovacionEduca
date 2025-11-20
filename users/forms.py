from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import CustomUser, Profesor, Estudiante, Directivo, Acudiente
from notas.models import Grado, Materia
from django.contrib.auth.forms import UserChangeForm


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


class EstudianteCreationForm(UserCreationForm):
    """
    Formulario para crear un nuevo estudiante con grado y materias asignadas.
    """
    first_name = forms.CharField(
        max_length=50,
        required=True,
        label="Nombre",
        validators=[RegexValidator(r'^[a-zA-Z\s]+$', 'Solo letras y espacios permitidos.')],
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'})
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        label="Apellido",
        validators=[RegexValidator(r'^[a-zA-Z\s]+$', 'Solo letras y espacios permitidos.')],
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'})
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'}),
        help_text="Mínimo 8 caracteres."
    )
    password2 = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'})
    )
    fecha_nacimiento = forms.DateField(
        required=True,
        label="Fecha de Nacimiento",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'})
    )
    grado = forms.ModelChoiceField(
        queryset=Grado.objects.all(),
        required=True,
        label="Grado Académico",
        widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'})
    )
    materias = forms.ModelMultipleChoiceField(
        queryset=Materia.objects.none(),  # Se cargará dinámicamente
        required=True,
        label="Materias",
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'space-y-2'}),
        help_text="Selecciona al menos una materia."
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'fecha_nacimiento', 'grado', 'materias')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Fijar tipo_usuario a estudiante
        self.instance.tipo_usuario = 'estudiante'
        # Cargar grados disponibles
        self.fields['grado'].queryset = Grado.objects.all().order_by('nombre')
        # Materias inicialmente vacío, se cargará con AJAX
        self.fields['materias'].queryset = Materia.objects.none()

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError('La contraseña debe tener al menos 8 caracteres.')
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Este email ya está registrado.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        grado = cleaned_data.get('grado')
        materias = cleaned_data.get('materias')
        if grado and materias:
            # Verificar que las materias pertenezcan al grado seleccionado
            grado_materias = set(Materia.objects.filter(grado=grado).values_list('id', flat=True))
            selected_materias = set(m.id for m in materias)
            if not selected_materias.issubset(grado_materias):
                raise ValidationError('Todas las materias seleccionadas deben pertenecer al grado elegido.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo_usuario = 'estudiante'
        user.fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        # Generar username
        base_username = f"{self.cleaned_data['first_name'].lower()}.{self.cleaned_data['last_name'].lower()}"
        username = base_username
        counter = 1
        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        user.username = username

        if commit:
            user.save()
            estudiante = Estudiante.objects.create(
                user=user,
                grado=self.cleaned_data.get('grado')
            )
            estudiante.materias.set(self.cleaned_data.get('materias'))
        return user


class CrearUsuarioForm(UserCreationForm):
    """
    Formulario para crear un usuario general (profesor, estudiante, directivo, acudiente).
    """
    first_name = forms.CharField(
        max_length=50,
        required=True,
        label="Nombre",
        validators=[RegexValidator(r'^[a-zA-Z\s]+$', 'Solo letras y espacios permitidos.')],
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'})
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        label="Apellido",
        validators=[RegexValidator(r'^[a-zA-Z\s]+$', 'Solo letras y espacios permitidos.')],
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'})
    )
    telefono = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'})
    )
    direccion = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'})
    )
    fecha_nacimiento = forms.DateField(
        required=True,
        label="Fecha de Nacimiento",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'})
    )
    tipo_usuario = forms.ChoiceField(
        choices=CustomUser.TIPO_USUARIO_CHOICES,
        required=True,
        label="Tipo de Usuario",
        widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'})
    )
    # Campos condicionales
    grado = forms.ModelChoiceField(
        queryset=Grado.objects.all(),
        required=False,
        label="Grado Académico",
        widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'})
    )
    materias = forms.ModelMultipleChoiceField(
        queryset=Materia.objects.all(),
        required=False,
        label="Materias",
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'space-y-2'}),
        help_text="Selecciona las materias."
    )
    estudiante_acudiente = forms.ModelChoiceField(
        queryset=Estudiante.objects.all(),
        required=False,
        label="Estudiante",
        widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'})
    )
    escuela = forms.CharField(
        max_length=100,
        required=False,
        label="Escuela",
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'})
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'telefono', 'direccion', 'fecha_nacimiento', 'tipo_usuario', 'grado', 'materias', 'estudiante_acudiente', 'escuela')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grado'].queryset = Grado.objects.all().order_by('nombre')
        self.fields['materias'].queryset = Materia.objects.all().order_by('nombre')
        self.fields['estudiante_acudiente'].queryset = Estudiante.objects.select_related('user').all()

        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            if field_name == 'tipo_usuario':
                field.widget.attrs['class'] += ' appearance-none'

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError('La contraseña debe tener al menos 8 caracteres.')
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Este email ya está registrado.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo_usuario')
        if tipo == 'estudiante':
            if not cleaned_data.get('grado'):
                raise ValidationError('El grado es requerido para estudiantes.')
        elif tipo == 'acudiente':
            if not cleaned_data.get('estudiante_acudiente'):
                raise ValidationError('Debe seleccionar un estudiante para el acudiente.')
        elif tipo == 'directivo':
            if not cleaned_data.get('escuela'):
                raise ValidationError('La escuela es requerida para directivos.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        user.telefono = self.cleaned_data.get('telefono')
        user.direccion = self.cleaned_data.get('direccion')
        tipo = self.cleaned_data.get('tipo_usuario')
        # Generar username
        base_username = f"{self.cleaned_data['first_name'].lower()}.{self.cleaned_data['last_name'].lower()}"
        username = base_username
        counter = 1
        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        user.username = username

        if commit:
            user.save()
            if tipo == 'estudiante':
                estudiante = Estudiante.objects.create(
                    user=user,
                    grado=self.cleaned_data.get('grado')
                )
                # Asignar todas las materias del grado al estudiante
                materias_grado = Materia.objects.filter(grado=self.cleaned_data.get('grado'))
                estudiante.materias.set(materias_grado)
            elif tipo == 'profesor':
                profesor = Profesor.objects.create(user=user)
                # Asignar materias al profesor
                for materia in self.cleaned_data.get('materias', []):
                    materia.profesor = profesor
                    materia.save()
            elif tipo == 'acudiente':
                acudiente = Acudiente.objects.create(user=user)
                estudiante = self.cleaned_data.get('estudiante_acudiente')
                if estudiante:
                    estudiante.acudiente = acudiente
                    estudiante.save()
            elif tipo == 'directivo':
                Directivo.objects.create(user=user, escuela=self.cleaned_data.get('escuela'))
        return user


class CustomUserChangeForm(UserChangeForm):
    """
    Formulario para editar un usuario existente.
    """
    password = None  # No mostrar campo de contraseña

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'tipo_usuario', 'is_active', 'telefono', 'direccion', 'fecha_nacimiento', 'nombre_colegio')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellido"
        self.fields['tipo_usuario'].label = "Tipo de Usuario"
        self.fields['is_active'].label = "Activo"
        self.fields['telefono'].label = "Teléfono"
        self.fields['direccion'].label = "Dirección"
        self.fields['fecha_nacimiento'].label = "Fecha de Nacimiento"
        self.fields['nombre_colegio'].label = "Nombre del Colegio"

        # Campos condicionales basados en tipo_usuario
        if self.instance and self.instance.pk:
            if self.instance.tipo_usuario == 'profesor':
                # Para profesor: selector de grado y materias
                profesor = getattr(self.instance, 'profesor_profile', None)
                initial_materias = []
                initial_grado = None
                if profesor:
                    materias_profesor = Materia.objects.filter(profesor=profesor).select_related('grado')
                    initial_materias = list(materias_profesor.values_list('id', flat=True))
                    # Set initial grade to the first grade of assigned subjects, if any
                    if materias_profesor.exists():
                        initial_grado = materias_profesor.first().grado
                self.fields['grado_profesor'] = forms.ModelChoiceField(
                    queryset=Grado.objects.all().order_by('nombre'),
                    required=False,
                    label="Grado para asignar materias",
                    widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'id': 'id_grado_profesor'}),
                    initial=initial_grado
                )
                self.fields['materias_profesor'] = forms.ModelMultipleChoiceField(
                    queryset=Materia.objects.all().order_by('grado__nombre', 'nombre'),
                    required=False,
                    label="Materias que imparte",
                    widget=forms.CheckboxSelectMultiple(attrs={'class': 'space-y-2', 'id': 'id_materias_profesor'}),
                    initial=initial_materias
                )
            elif self.instance.tipo_usuario == 'estudiante':
                # Para estudiante: grado y acudiente
                estudiante = getattr(self.instance, 'estudiante_profile', None)
                initial_grado = None
                initial_acudiente = None
                if estudiante:
                    initial_grado = estudiante.grado
                    initial_acudiente = estudiante.acudiente
                self.fields['grado_estudiante'] = forms.ModelChoiceField(
                    queryset=Grado.objects.all().order_by('nombre'),
                    required=False,
                    label="Grado",
                    widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'}),
                    initial=initial_grado
                )
                self.fields['acudiente_estudiante'] = forms.ModelChoiceField(
                    queryset=Acudiente.objects.all(),
                    required=False,
                    label="Acudiente",
                    widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'}),
                    initial=initial_acudiente
                )

        for field_name, field in self.fields.items():
            if field_name == 'fecha_nacimiento':
                field.widget = forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'})
            else:
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
                })

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Guardar campos condicionales
            if user.tipo_usuario == 'profesor' and hasattr(user, 'profesor_profile'):
                profesor = user.profesor_profile
                if 'materias_profesor' in self.cleaned_data:
                    # Asignar profesor a las materias seleccionadas
                    Materia.objects.filter(profesor=profesor).update(profesor=None)  # Limpiar asignaciones previas
                    for materia in self.cleaned_data['materias_profesor']:
                        materia.profesor = profesor
                        materia.save()
            elif user.tipo_usuario == 'estudiante' and hasattr(user, 'estudiante_profile'):
                estudiante = user.estudiante_profile
                if 'grado_estudiante' in self.cleaned_data:
                    estudiante.grado = self.cleaned_data['grado_estudiante']
                if 'acudiente_estudiante' in self.cleaned_data:
                    estudiante.acudiente = self.cleaned_data['acudiente_estudiante']
                estudiante.save()
        return user