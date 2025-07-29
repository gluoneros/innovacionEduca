from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profesor, Estudiante, Directivo, Acudiente

# Registra tus modelos aquí para que aparezcan en el panel de admin.

class CustomUserAdmin(UserAdmin):
    # Añade tus campos personalizados al admin
    fieldsets = UserAdmin.fieldsets + (
        ('Campos Personalizados', {'fields': ('tipo_usuario', 'documento', 'telefono', 'fecha_nacimiento', 'nombre_colegio')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Campos Personalizados', {'fields': ('tipo_usuario', 'documento', 'telefono', 'fecha_nacimiento', 'nombre_colegio', 'first_name', 'last_name', 'email')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profesor)
admin.site.register(Estudiante)
admin.site.register(Directivo)
admin.site.register(Acudiente)