from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import EscalaNota, AnioEscolar, Grado, Materia, Periodo, Nota, InformeFinal
from users.models import Profesor, Estudiante

from django.db.models import Q, Sum, F
from django.http import JsonResponse
from django.db import transaction
from django.core.exceptions import ValidationError
import json



from .forms import (
    EscalaNotaForm, AnioEscolarForm, GradoForm, MateriaForm, 
    PeriodoForm, NotaForm, InformeFinalForm, BuscarEstudianteForm, 
    BuscarNotaForm, ImportarNotasForm
)
#---------------------========================Qwen==mas escalable y legible======================================0
#============================0====VISTA BASADA EN CLASES======================================================
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import EscalaNota
from .forms import EscalaNotaForm  # Asumiendo que crearás un formulario

# Lista de escalas
class EscalaNotaListView(ListView):
    model = EscalaNota
    template_name = 'escalanota/lista.html'
    context_object_name = 'escalas'

# Crear nueva escala
class EscalaNotaCreateView(CreateView):
    model = EscalaNota
    form_class = EscalaNotaForm
    template_name = 'escalanota/form.html'
    success_url = reverse_lazy('escala_lista')

# Editar escala existente
class EscalaNotaUpdateView(UpdateView):
    model = EscalaNota
    form_class = EscalaNotaForm
    template_name = 'escalanota/form.html'
    success_url = reverse_lazy('escala_lista')

# Eliminar escala
class EscalaNotaDeleteView(DeleteView):
    model = EscalaNota
    template_name = 'escalanota/confirmar_eliminar.html'
    success_url = reverse_lazy('escala_lista')




#===========================================0menos escalable==========================================00=======
#====================================VISTA BASADA EN FUNCIONES=====================================================0



@login_required
def lista_escalas(request):
    escalas = EscalaNota.objects.all()
    return render(request, 'notas/escalas/lista.html', {'escalas': escalas})


@login_required
def crear_escala(request):
    if request.method == 'POST':
        form = EscalaNotaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Escala creada exitosamente.')
            return redirect('notas:lista_escalas')
    else:
        form = EscalaNotaForm()
    return render(request, 'notas/escalas/crear.html', {'form': form})


@login_required
def editar_escala(request, pk):
    escala = get_object_or_404(EscalaNota, pk=pk)
    if request.method == 'POST':
        form = EscalaNotaForm(request.POST, instance=escala)
        if form.is_valid():
            form.save()
            messages.success(request, 'Escala actualizada exitosamente.')
            return redirect('notas:lista_escalas')
    else:
        form = EscalaNotaForm(instance=escala)
    return render(request, 'notas/escalas/editar.html', {'form': form, 'escala': escala})


@login_required
def lista_anios_escolares(request):
    anios = AnioEscolar.objects.all().order_by('-anio')
    return render(request, 'notas/anios/lista.html', {'anios': anios})


@login_required
def crear_anio_escolar(request):
    if request.method == 'POST':
        form = AnioEscolarForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Año escolar creado exitosamente.')
            return redirect('notas:lista_anios')
    else:
        form = AnioEscolarForm()
    return render(request, 'notas/anios/crear.html', {'form': form})


@login_required
def lista_grados(request):
    grados = Grado.objects.all().order_by('nombre')
    return render(request, 'notas/grados/lista.html', {'grados': grados})


@login_required
def crear_grado(request):
    if request.method == 'POST':
        form = GradoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grado creado exitosamente.')
            return redirect('notas:lista_grados')
    else:
        form = GradoForm()
    return render(request, 'notas/grados/crear.html', {'form': form})


@login_required
def lista_materias(request):
    materias = Materia.objects.select_related('grado', 'profesor').all()
    
    # Filtros
    form_busqueda = BuscarEstudianteForm(request.GET)
    if form_busqueda.is_valid():
        nombre = form_busqueda.cleaned_data.get('nombre')
        grado = form_busqueda.cleaned_data.get('grado')
        
        if nombre:
            materias = materias.filter(nombre__icontains=nombre)
        if grado:
            materias = materias.filter(grado=grado)
    
    paginator = Paginator(materias, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'notas/materias/lista.html', {
        'page_obj': page_obj,
        'form_busqueda': form_busqueda
    })


@login_required
def crear_materia(request):
    if request.method == 'POST':
        form = MateriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Materia creada exitosamente.')
            return redirect('notas:lista_materias')
    else:
        form = MateriaForm()
    return render(request, 'notas/materias/crear.html', {'form': form})


@login_required
def editar_materia(request, pk):
    materia = get_object_or_404(Materia, pk=pk)
    if request.method == 'POST':
        form = MateriaForm(request.POST, instance=materia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Materia actualizada exitosamente.')
            return redirect('notas:lista_materias')
    else:
        form = MateriaForm(instance=materia)
    return render(request, 'notas/materias/editar.html', {'form': form, 'materia': materia})


@login_required
def lista_periodos(request):
    periodos = Periodo.objects.select_related('anio_escolar').all().order_by('anio_escolar__anio', 'nombre')
    return render(request, 'notas/periodos/lista.html', {'periodos': periodos})


@login_required
def crear_periodo(request):
    if request.method == 'POST':
        form = PeriodoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Período creado exitosamente.')
            return redirect('notas:lista_periodos')
    else:
        form = PeriodoForm()
    return render(request, 'notas/periodos/crear.html', {'form': form})


@login_required
def lista_notas(request):
    notas = Nota.objects.select_related('estudiante', 'materia', 'periodo').all()
    
    # Filtros
    form_busqueda = BuscarNotaForm(request.GET)
    if form_busqueda.is_valid():
        estudiante = form_busqueda.cleaned_data.get('estudiante')
        materia = form_busqueda.cleaned_data.get('materia')
        periodo = form_busqueda.cleaned_data.get('periodo')
        
        if estudiante:
            notas = notas.filter(estudiante=estudiante)
        if materia:
            notas = notas.filter(materia=materia)
        if periodo:
            notas = notas.filter(periodo=periodo)
    
    paginator = Paginator(notas, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'notas/notas/lista.html', {
        'page_obj': page_obj,
        'form_busqueda': form_busqueda
    })


@login_required
def crear_nota(request):
    if request.method == 'POST':
        form = NotaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nota creada exitosamente.')
            return redirect('notas:lista_notas')
    else:
        form = NotaForm()
    return render(request, 'notas/notas/crear.html', {'form': form})


@login_required
def editar_nota(request, pk):
    nota = get_object_or_404(Nota, pk=pk)
    if request.method == 'POST':
        form = NotaForm(request.POST, instance=nota)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nota actualizada exitosamente.')
            return redirect('notas:lista_notas')
    else:
        form = NotaForm(instance=nota)
    return render(request, 'notas/notas/editar.html', {'form': form, 'nota': nota})


@login_required
def eliminar_nota(request, pk):
    nota = get_object_or_404(Nota, pk=pk)
    if request.method == 'POST':
        nota.delete()
        messages.success(request, 'Nota eliminada exitosamente.')
        return redirect('notas:lista_notas')
    return render(request, 'notas/notas/eliminar.html', {'nota': nota})


@login_required
def importar_notas(request):
    if request.method == 'POST':
        form = ImportarNotasForm(request.POST, request.FILES)
        if form.is_valid():
            # Aquí implementarías la lógica para procesar el archivo
            # Por ejemplo, usando pandas para leer Excel/CSV
            messages.success(request, 'Notas importadas exitosamente.')
            return redirect('notas:lista_notas')
    else:
        form = ImportarNotasForm()
    return render(request, 'notas/notas/importar.html', {'form': form})


@login_required
def lista_informes_finales(request):
    informes = InformeFinal.objects.select_related('estudiante', 'materia', 'anio_escolar').all()
    return render(request, 'notas/informes/lista.html', {'informes': informes})


@login_required
def crear_informe_final(request):
    if request.method == 'POST':
        form = InformeFinalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Informe final creado exitosamente.')
            return redirect('notas:lista_informes')
    else:
        form = InformeFinalForm()
    return render(request, 'notas/informes/crear.html', {'form': form})

#--------------------------------------------------------------Extras para manejo masivo de notas sonet----
# Agregar esta vista a tu views.py existente

from django.http import JsonResponse
from django.db import transaction
import json


@login_required
def cursos_directivo(request):
    """Vista principal para la gestión de cursos por el directivo"""
    # Obtener datos iniciales
    anios_escolares = AnioEscolar.objects.all().order_by('-anio')
    escalas = EscalaNota.objects.all()
    grados = Grado.objects.all().order_by('nombre')
    materias = Materia.objects.select_related('grado', 'profesor').all()
    profesores = Profesor.objects.filter(user__is_active=True)

    # Año escolar activo por defecto
    anio_activo = anios_escolares.filter(activo=True).first()

    context = {
        'anios_escolares': anios_escolares,
        'escalas': escalas,
        'grados': grados,
        'materias': materias,
        'profesores': profesores,
        'anio_activo': anio_activo,
    }

    return render(request, 'notas/cursos_directivo.html', context)


@login_required
def crear_anio_escolar_ajax(request):
    """Crear año escolar vía AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            anio = data.get('anio')
            escala_id = data.get('escala_id')
            activo = data.get('activo', False)

            # Validar que el año no existe
            if AnioEscolar.objects.filter(anio=anio).exists():
                return JsonResponse({
                    'success': False,
                    'error': f'El año {anio} ya existe'
                })

            # Crear el año escolar
            anio_escolar = AnioEscolar.objects.create(
                anio=anio,
                escala_id=escala_id,
                activo=activo
            )

            return JsonResponse({
                'success': True,
                'anio_escolar': {
                    'id': anio_escolar.id,
                    'anio': anio_escolar.anio,
                    'activo': anio_escolar.activo,
                    'escala_nombre': anio_escolar.escala.nombre
                }
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método no permitido'})


@login_required
def crear_grado_ajax(request):
    """Crear grado vía AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre')
            anio_id = data.get('anio_id')

            # Validar que el grado no existe para ese año
            if Grado.objects.filter(nombre=nombre, anio_id=anio_id).exists():
                return JsonResponse({
                    'success': False,
                    'error': f'El grado {nombre} ya existe para este año'
                })

            # Crear el grado
            grado = Grado.objects.create(
                nombre=nombre,
                anio_id=anio_id if anio_id else None
            )

            return JsonResponse({
                'success': True,
                'grado': {
                    'id': grado.id,
                    'nombre': grado.nombre,
                    'anio': grado.anio.anio if grado.anio else None
                }
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método no permitido'})


@login_required
def crear_materia_ajax(request):
    """Crear materia vía AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre')
            grado_id = data.get('grado_id')
            profesor_id = data.get('profesor_id')

            # Validar que la materia no existe para ese grado
            if Materia.objects.filter(nombre=nombre, grado_id=grado_id).exists():
                return JsonResponse({
                    'success': False,
                    'error': f'La materia {nombre} ya existe para este grado'
                })

            # Crear la materia
            materia = Materia.objects.create(
                nombre=nombre,
                grado_id=grado_id if grado_id else None,
                profesor_id=profesor_id if profesor_id else None
            )

            return JsonResponse({
                'success': True,
                'materia': {
                    'id': materia.id,
                    'nombre': materia.nombre,
                    'grado': materia.grado.nombre if materia.grado else None,
                    'profesor': f"{materia.profesor.user.first_name} {materia.profesor.user.last_name}" if materia.profesor else None
                }
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método no permitido'})


@login_required
def crear_escala_ajax(request):
    """Crear escala de notas vía AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre')
            minimo = float(data.get('minimo'))
            maximo = float(data.get('maximo'))
            paso = float(data.get('paso', 0.1))

            # Validaciones
            if minimo >= maximo:
                return JsonResponse({
                    'success': False,
                    'error': 'El valor mínimo debe ser menor que el máximo'
                })

            if EscalaNota.objects.filter(nombre=nombre).exists():
                return JsonResponse({
                    'success': False,
                    'error': f'La escala {nombre} ya existe'
                })

            # Crear la escala
            escala = EscalaNota.objects.create(
                nombre=nombre,
                minimo=minimo,
                maximo=maximo,
                paso=paso
            )

            return JsonResponse({
                'success': True,
                'escala': {
                    'id': escala.id,
                    'nombre': escala.nombre,
                    'minimo': float(escala.minimo),
                    'maximo': float(escala.maximo),
                    'paso': float(escala.paso)
                }
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método no permitido'})


@login_required
def obtener_datos_anio(request, anio_id):
    """Obtener grados y materias de un año específico"""
    try:
        anio = get_object_or_404(AnioEscolar, id=anio_id)
        grados = Grado.objects.filter(anio=anio)
        materias = Materia.objects.filter(grado__anio=anio).select_related('grado', 'profesor')

        grados_data = [{'id': g.id, 'nombre': g.nombre} for g in grados]
        materias_data = [{
            'id': m.id,
            'nombre': m.nombre,
            'grado': m.grado.nombre if m.grado else None,
            'grado_id': m.grado.id if m.grado else None,
            'profesor': f"{m.profesor.user.first_name} {m.profesor.user.last_name}" if m.profesor else None,
            'profesor_id': m.profesor.id if m.profesor else None
        } for m in materias]

        return JsonResponse({
            'success': True,
            'anio': {
                'id': anio.id,
                'anio': anio.anio,
                'escala': anio.escala.nombre
            },
            'grados': grados_data,
            'materias': materias_data
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# Agregar estas funciones adicionales a tu views.py


@login_required
def eliminar_materia_ajax(request, materia_id):
    """Eliminar materia vía AJAX"""
    if request.method == 'DELETE':
        try:
            materia = get_object_or_404(Materia, id=materia_id)

            # Verificar si la materia tiene notas asociadas
            if materia.notas.exists():
                return JsonResponse({
                    'success': False,
                    'error': 'No se puede eliminar la materia porque tiene notas asociadas'
                })

            nombre_materia = materia.nombre
            materia.delete()

            return JsonResponse({
                'success': True,
                'message': f'Materia {nombre_materia} eliminada exitosamente'
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método no permitido'})


@login_required
def activar_anio_escolar(request, anio_id):
    """Activar un año escolar específico"""
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Desactivar todos los años
                AnioEscolar.objects.all().update(activo=False)

                # Activar el año seleccionado
                anio = get_object_or_404(AnioEscolar, id=anio_id)
                anio.activo = True
                anio.save()

                return JsonResponse({
                    'success': True,
                    'message': f'Año {anio.anio} activado exitosamente'
                })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método no permitido'})


@login_required
def obtener_materia_ajax(request, materia_id):
    """Obtener datos de una materia específica para edición"""
    try:
        materia = get_object_or_404(Materia, id=materia_id)

        return JsonResponse({
            'success': True,
            'materia': {
                'id': materia.id,
                'nombre': materia.nombre,
                'grado_id': materia.grado.id if materia.grado else None,
                'grado_nombre': materia.grado.nombre if materia.grado else None,
                'profesor_id': materia.profesor.id if materia.profesor else None,
                'profesor_nombre': f"{materia.profesor.user.first_name} {materia.profesor.user.last_name}" if materia.profesor else None
            }
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def crear_periodo_ajax(request):
    """Crear período vía AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            anio_escolar_id = data.get('anio_escolar_id')
            nombre = data.get('nombre')
            porcentaje = float(data.get('porcentaje'))

            # Validar que el período no exista
            if Periodo.objects.filter(anio_escolar_id=anio_escolar_id, nombre=nombre).exists():
                return JsonResponse({
                    'success': False,
                    'error': f'El período {nombre} ya existe para este año'
                })

            # Validar suma de porcentajes
            total_porcentajes = Periodo.objects.filter(
                anio_escolar_id=anio_escolar_id
            ).aggregate(suma=Sum('porcentaje'))['suma'] or 0

            if total_porcentajes + porcentaje > 100:
                return JsonResponse({
                    'success': False,
                    'error': 'La suma de los porcentajes no puede superar 100%'
                })

            # Crear el período
            periodo = Periodo.objects.create(
                anio_escolar_id=anio_escolar_id,
                nombre=nombre,
                porcentaje=porcentaje
            )

            return JsonResponse({
                'success': True,
                'periodo': {
                    'id': periodo.id,
                    'nombre': periodo.nombre,
                    'porcentaje': float(periodo.porcentaje),
                    'anio_escolar': periodo.anio_escolar.anio
                }
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método no permitido'})


@login_required
def obtener_estadisticas_anio(request, anio_id):
    """Obtener estadísticas del año escolar"""
    try:
        anio = get_object_or_404(AnioEscolar, id=anio_id)

        # Contar grados
        total_grados = Grado.objects.filter(anio=anio).count()

        # Contar materias
        total_materias = Materia.objects.filter(grado__anio=anio).count()

        # Contar estudiantes matriculados en el año
        total_estudiantes = Estudiante.objects.filter(
            user__is_active=True,
            # Aquí puedes agregar filtro por matrícula si tienes ese modelo
        ).count()

        # Contar profesores asignados
        profesores_asignados = Materia.objects.filter(
            grado__anio=anio,
            profesor__isnull=False
        ).values('profesor').distinct().count()

        # Contar períodos
        total_periodos = Periodo.objects.filter(anio_escolar=anio).count()
        suma_porcentajes = Periodo.objects.filter(anio_escolar=anio).aggregate(
            suma=Sum('porcentaje')
        )['suma'] or 0

        return JsonResponse({
            'success': True,
            'estadisticas': {
                'anio': anio.anio,
                'escala': anio.escala.nombre,
                'total_grados': total_grados,
                'total_materias': total_materias,
                'total_estudiantes': total_estudiantes,
                'profesores_asignados': profesores_asignados,
                'total_periodos': total_periodos,
                'suma_porcentajes': float(suma_porcentajes),
                'porcentajes_completos': suma_porcentajes == 100
            }
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# Agregar estas funciones adicionales a tu views.py

@login_required
def editar_materia_ajax(request, materia_id):
    """Editar materia vía AJAX"""
    if request.method == 'POST':
        try:
            materia = get_object_or_404(Materia, id=materia_id)
            data = json.loads(request.body)

            nombre = data.get('nombre')
            grado_id = data.get('grado_id')
            profesor_id = data.get('profesor_id')

            # Validar que no exista otra materia con el mismo nombre en el mismo grado
            if Materia.objects.filter(
                    nombre=nombre,
                    grado_id=grado_id
            ).exclude(id=materia_id).exists():
                return JsonResponse({
                    'success': False,
                    'error': f'La materia {nombre} ya existe para este grado'
                })

            # Actualizar la materia
            materia.nombre = nombre
            materia.grado_id = grado_id if grado_id else None
            materia.profesor_id = profesor_id if profesor_id else None
            materia.save()

            return JsonResponse({
                'success': True,
                'materia': {
                    'id': materia.id,
                    'nombre': materia.nombre,
                    'grado': materia.grado.nombre if materia.grado else None,
                    'profesor': f"{materia.profesor.user.first_name} {materia.profesor.user.last_name}" if materia.profesor else None
                }
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método no permitido'})


@login_required
def eliminar_materia_ajax(request, materia_id):
    """Eliminar materia vía AJAX"""
    if request.method == 'DELETE':
        try:
            materia = get_object_or_404(Materia, id=materia_id)

            # Verificar si la materia tiene notas asociadas
            if materia.notas.exists():
                return JsonResponse({
                    'success': False,
                    'error': 'No se puede eliminar la materia porque tiene notas asociadas'
                })

            nombre_materia = materia.nombre
            materia.delete()

            return JsonResponse({
                'success': True,
                'message': f'Materia {nombre_materia} eliminada exitosamente'
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método no permitido'})


@login_required
def activar_anio_escolar(request, anio_id):
    """Activar un año escolar específico"""
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Desactivar todos los años
                AnioEscolar.objects.all().update(activo=False)

                # Activar el año seleccionado
                anio = get_object_or_404(AnioEscolar, id=anio_id)
                anio.activo = True
                anio.save()

                return JsonResponse({
                    'success': True,
                    'message': f'Año {anio.anio} activado exitosamente'
                })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@login_required
def crear_periodo_ajax(request):
    """Crear período vía AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            anio_escolar_id = data.get('anio_escolar_id')
            nombre = data.get('nombre')
            porcentaje = float(data.get('porcentaje'))

            # Validar que el período no exista
            if Periodo.objects.filter(anio_escolar_id=anio_escolar_id, nombre=nombre).exists():
                return JsonResponse({
                    'success': False,
                    'error': f'El período {nombre} ya existe para este año'
                })

            # Validar suma de porcentajes
            total_porcentajes = Periodo.objects.filter(
                anio_escolar_id=anio_escolar_id
            ).aggregate(suma=Sum('porcentaje'))['suma'] or 0

            if total_porcentajes + porcentaje > 100:
                return JsonResponse({
                    'success': False,
                    'error': 'La suma de los porcentajes no puede superar 100%'
                })

            # Crear el período
            periodo = Periodo.objects.create(
                anio_escolar_id=anio_escolar_id,
                nombre=nombre,
                porcentaje=porcentaje
            )

            return JsonResponse({
                'success': True,
                'periodo': {
                    'id': periodo.id,
                    'nombre': periodo.nombre,
                    'porcentaje': float(periodo.porcentaje),
                    'anio_escolar': periodo.anio_escolar.anio
                }
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método no permitido'})


@login_required
def obtener_estadisticas_anio(request, anio_id):
    """Obtener estadísticas del año escolar"""
    try:
        anio = get_object_or_404(AnioEscolar, id=anio_id)

        # Contar grados
        total_grados = Grado.objects.filter(anio=anio).count()

        # Contar materias
        total_materias = Materia.objects.filter(grado__anio=anio).count()

        # Contar estudiantes matriculados en el año
        total_estudiantes = Estudiante.objects.filter(
            user__is_active=True,
            # Aquí puedes agregar filtro por matrícula si tienes ese modelo
        ).count()

        # Contar profesores asignados
        profesores_asignados = Materia.objects.filter(
            grado__anio=anio,
            profesor__isnull=False
        ).values('profesor').distinct().count()

        # Contar períodos
        total_periodos = Periodo.objects.filter(anio_escolar=anio).count()
        suma_porcentajes = Periodo.objects.filter(anio_escolar=anio).aggregate(
            suma=Sum('porcentaje')
        )['suma'] or 0

        return JsonResponse({
            'success': True,
            'estadisticas': {
                'anio': anio.anio,
                'escala': anio.escala.nombre,
                'total_grados': total_grados,
                'total_materias': total_materias,
                'total_estudiantes': total_estudiantes,
                'profesores_asignados': profesores_asignados,
                'total_periodos': total_periodos,
                'suma_porcentajes': float(suma_porcentajes),
                'porcentajes_completos': suma_porcentajes == 100
            }
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
