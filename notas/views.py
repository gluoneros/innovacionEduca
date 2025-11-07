from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import  AnioEscolar, Grado, Materia, Periodo, Nota, InformeFinal
from users.models import Profesor, Estudiante

from django.db.models import Q, Sum, F
from django.http import JsonResponse
from django.core.exceptions import ValidationError
import json

from .forms import (
    EscalaNotaForm, AnioEscolarForm, GradoForm, MateriaForm,
    PeriodoForm, NotaForm, InformeFinalForm, BuscarEstudianteForm,
    BuscarNotaForm, ImportarNotasForm, PeriodoFormSet
)

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy

from .forms import EscalaNotaForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import EscalaNota, ESCALAS_PREDEFINIDAS

from django.views import View


#==============================================Escalas de notas==============================================
#------------------------------------------------------------------------------------------------------------
# Crear nueva escala
class EscalaNotaCreateView(LoginRequiredMixin, CreateView):
    model = EscalaNota
    form_class = EscalaNotaForm
    template_name = 'notas/escalas/form.html'
    success_url = reverse_lazy('escala_lista')

# Editar escala existente
class EscalaNotaUpdateView(LoginRequiredMixin, UpdateView):
    model = EscalaNota
    form_class = EscalaNotaForm
    template_name = 'notas/escalas/form.html'
    success_url = reverse_lazy('escala_lista')

# Eliminar escala
class EscalaNotaDeleteView(LoginRequiredMixin, DeleteView):
    model = EscalaNota
    template_name = 'notas/escalas/confirmar_eliminar.html'
    success_url = reverse_lazy('escala_lista')

# Listar escalas
class EscalaNotaListView(LoginRequiredMixin, ListView):
    model = EscalaNota
    template_name = 'notas/escala/lista.html'
    context_object_name = 'escalas'

    def get_queryset(self):
        # Asegurar que las escalas predefinidas existan
        for nombre, min_val, max_val in ESCALAS_PREDEFINIDAS:
            EscalaNota.objects.get_or_create(
                nombre=nombre,
                ddefaults={'minimo': min_val, 'maximo': max_val, 'paso': 0.01, 'es_predefinida': True}
            )
        return super().get_queryset()



#==============================================Años escolares================================================
#------------------------------------------------------------------------------------------------------------
class AnioEscolarCreateView(LoginRequiredMixin, CreateView):
    model = AnioEscolar
    form_class = AnioEscolarForm
    template_name = 'notas/anios/crear.html'
    success_url = reverse_lazy('notas:lista_anios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['periodo_formset'] = PeriodoFormSet(self.request.POST, instance=self.object)
        else:
            context['periodo_formset'] = PeriodoFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        periodo_formset = context['periodo_formset']

        # Validación: Solo puede haber un año activo a la vez
        if form.cleaned_data.get('activo', False):
            anio_activo_existente = AnioEscolar.objects.filter(activo=True).first()

            if anio_activo_existente:
                messages.error(self.request,
                    f'No se puede crear un año escolar activo porque ya existe el año {anio_activo_existente.anio} activo. '
                    f'Solo puede haber un año escolar activo a la vez. '
                    f'Primero desactiva el año {anio_activo_existente.anio} o crea este año como inactivo.'
                )
                return self.form_invalid(form)

        if periodo_formset.is_valid():
            try:
                with transaction.atomic():
                    # Guardar el año escolar
                    self.object = form.save()

                    # Guardar los periodos
                    periodo_formset.instance = self.object
                    periodo_formset.save()

                if self.object.activo:
                    messages.success(self.request, f'Año escolar {self.object.anio} creado y activado con {periodo_formset.forms} periodos.')
                else:
                    messages.success(self.request, f'Año escolar {self.object.anio} creado como inactivo con periodos.')
                return super().form_valid(form)

            except Exception as e:
                messages.error(self.request, f'Error al crear el año escolar: {str(e)}')
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)

# Vista para editar solo el estado activo de un año escolar
class EditarEstadoAnioView(LoginRequiredMixin, View):
    template_name = 'notas/anios/editar_estado.html'

    def get(self, request, pk):
        anio = get_object_or_404(AnioEscolar, pk=pk)
        return render(request, self.template_name, {'anio': anio})

    def post(self, request, pk):
        anio = get_object_or_404(AnioEscolar, pk=pk)
        nuevo_estado = request.POST.get('activo') == 'on'
        
        # Validación: Solo puede haber un año activo a la vez
        if nuevo_estado:
            anio_activo_existente = AnioEscolar.objects.filter(activo=True).exclude(pk=pk).first()
            if anio_activo_existente:
                messages.error(
                    request,
                    f'No se puede activar el año {anio.anio} porque ya existe el año {anio_activo_existente.anio} activo. '
                    f'Solo puede haber un año escolar activo a la vez. '
                    f'Primero desactiva el año {anio_activo_existente.anio} si deseas activar este año.'
                )
                return render(request, self.template_name, {'anio': anio})

        # Actualizar el estado
        anio.activo = nuevo_estado
        anio.save()

        if nuevo_estado:
            messages.success(request, f'El año {anio.anio} ha sido activado correctamente.')
        else:
            messages.success(request, f'El año {anio.anio} ha sido desactivado correctamente.')

        return redirect('notas:lista_anios')

class EliminarAnioEscolarView(LoginRequiredMixin, View):
    def post(self, request, pk):
        anio = get_object_or_404(AnioEscolar, pk=pk)

        # Validación: no permitir eliminar si no es POST (aunque al usar post(), esto ya está cubierto)
        # pero mantenemos coherencia con la lógica original

        if anio.activo:
            messages.error(
                request,
                'No se puede eliminar un año escolar activo. Desactívelo antes de eliminarlo.'
            )
            return redirect('notas:lista_anios')

        grados_count = anio.grados.count()
        periodos_count = anio.periodos.count()
        informes_count = InformeFinal.objects.filter(anio_escolar=anio).count()
        notas_count = Nota.objects.filter(periodo__anio_escolar=anio).count()

        if grados_count or periodos_count or informes_count or notas_count:
            messages.error(
                request,
                (
                    'No se puede eliminar el año escolar porque tiene dependencias registradas: '
                    f'{grados_count} grado(s), {periodos_count} período(s), '
                    f'{informes_count} informe(s) final(es) y {notas_count} nota(s).'
                )
            )
            return redirect('notas:lista_anios')

        anio_valor = anio.anio
        anio.delete()
        messages.success(request, f'Año escolar {anio_valor} eliminado correctamente.')
        return redirect('notas:lista_anios')


#==============================================Períodos========================================================
#--------------------------------------------------------------------------------------------------------------
class CrearPeriodoView(LoginRequiredMixin, CreateView):
    model = Periodo
    form_class = PeriodoForm
    template_name = 'notas/periodos/crear.html'
    success_url = reverse_lazy('notas:lista_periodos')

    def form_valid(self, form):
        messages.success(self.request, 'Período creado exitosamente.')
        return super().form_valid(form)

class ListaPeriodosView(LoginRequiredMixin, ListView):
    model = Periodo
    template_name = 'notas/periodos/lista.html'
    context_object_name = 'periodos'
    ordering = ['anio_escolar__anio', 'nombre']

class GestionarAniosPeriodosView(LoginRequiredMixin, View):
    template_name = 'notas/anios/lista.html'

    def get(self, request):
        anios = (
            AnioEscolar.objects
            .prefetch_related('periodos', 'grados')
            .select_related('escala')
            .order_by('-anio')
        )
        anio_activo = anios.filter(activo=True).first()
        escalas_usadas = (
            EscalaNota.objects
            .filter(anios_escolares__in=anios)
            .distinct()
            .count()
        )

        context = {
            'anios': anios,
            'anio_form': AnioEscolarForm(),
            'periodo_form': PeriodoForm(),
            'anio_activo': anio_activo,
            'estadisticas': {
                'total_anios': anios.count(),
                'anio_activo': anio_activo.anio if anio_activo else None,
                'escalas_usadas': escalas_usadas,
            },
        }
        return render(request, self.template_name, context)

    def post(self, request):
        anios = (
            AnioEscolar.objects
            .prefetch_related('periodos', 'grados')
            .select_related('escala')
            .order_by('-anio')
        )
        anio_form = AnioEscolarForm()
        periodo_form = PeriodoForm()
        form_type = request.POST.get('form_type')

        if form_type == 'anio':
            anio_form = AnioEscolarForm(request.POST)
            periodo_form = PeriodoForm()  # Reset periodo_form

            if anio_form.is_valid():
                try:
                    nuevo_anio = anio_form.save()
                    messages.success(
                        request,
                        f'Año escolar {nuevo_anio.anio} creado correctamente.'
                    )
                    return redirect('notas:lista_anios')
                except ValidationError as error:
                    self._agregar_errores_formulario(anio_form, error)
            if anio_form.errors:
                messages.error(
                    request,
                    'Hay errores en el formulario de creación de año escolar.'
                )

        elif form_type == 'periodo':
            periodo_form = PeriodoForm(request.POST)
            anio_form = AnioEscolarForm()  # Reset anio_form

            if periodo_form.is_valid():
                try:
                    periodo = periodo_form.save()
                    messages.success(
                        request,
                        f'Período {periodo.nombre} creado para el año {periodo.anio_escolar.anio}.'
                    )
                    return redirect('notas:lista_anios')
                except ValidationError as error:
                    self._agregar_errores_formulario(periodo_form, error)
            if periodo_form.errors:
                messages.error(
                    request,
                    'Hay errores en el formulario de creación de período.'
                )
        else:
            messages.error(request, 'La acción solicitada no es válida.')
            return redirect('notas:lista_anios')

        # Si llegamos aquí, hubo errores o formularios inválidos
        anio_activo = anios.filter(activo=True).first()
        escalas_usadas = (
            EscalaNota.objects
            .filter(anios_escolares__in=anios)
            .distinct()
            .count()
        )

        context = {
            'anios': anios,
            'anio_form': anio_form,
            'periodo_form': periodo_form,
            'anio_activo': anio_activo,
            'estadisticas': {
                'total_anios': anios.count(),
                'anio_activo': anio_activo.anio if anio_activo else None,
                'escalas_usadas': escalas_usadas,
            },
        }
        return render(request, self.template_name, context)

    def _agregar_errores_formulario(self, form, error):
        """
        Método auxiliar para agregar errores de ValidationError a un formulario.
        """
        if hasattr(error, 'message_dict'):
            for field, mensajes in error.message_dict.items():
                destino = None if field in (None, '__all__') else field
                for mensaje in mensajes:
                    form.add_error(destino, mensaje)
        else:
            for mensaje in getattr(error, 'messages', [str(error)]):
                form.add_error(None, mensaje)
                
                
@login_required
def obtener_periodos_por_anio(request, anio_id):
    """Obtener periodos de un año escolar específico para filtrado dinámico"""
    try:
        anio = get_object_or_404(AnioEscolar, id=anio_id)
        periodos = Periodo.objects.filter(anio_escolar=anio).order_by('nombre')
        
        periodos_data = [{
            'id': p.id,
            'nombre': p.nombre,
            'porcentaje': float(p.porcentaje)
        } for p in periodos]
        
        return JsonResponse({
            'success': True,
            'periodos': periodos_data
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


#==============================================Grados========================================================
#------------------------------------------------------------------------------------------------------------
class ListaGradosView(LoginRequiredMixin, ListView):
    model = Grado
    template_name = 'notas/grados/lista.html'
    context_object_name = 'grados'
    ordering = ['nombre']

    def get_queryset(self):
        return Grado.objects.select_related('anio', 'periodo').prefetch_related('materias').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grados = self.get_queryset()
        total_grados = grados.count()
        grados_con_anio = sum(1 for grado in grados if grado.anio)
        total_materias = sum(grado.materias.count() for grado in grados)

        context.update({
            'total_grados': total_grados,
            'grados_con_anio': grados_con_anio,
            'total_materias': total_materias,
        })
        return context


class CrearGradoView(LoginRequiredMixin, CreateView):
    model = Grado
    form_class = GradoForm
    template_name = 'notas/grados/crear.html'
    success_url = reverse_lazy('notas:lista_grados')

    def form_valid(self, form):
        messages.success(self.request, 'Grado creado exitosamente.')
        return super().form_valid(form)


from django.views.generic import UpdateView

class EditarGradoView(LoginRequiredMixin, UpdateView):
    model = Grado
    form_class = GradoForm
    template_name = 'notas/grados/editar.html'
    success_url = reverse_lazy('notas:lista_grados')

    def form_valid(self, form):
        messages.success(self.request, 'Grado actualizado exitosamente.')
        return super().form_valid(form)

from django.views.generic import DeleteView


class EliminarGradoView(LoginRequiredMixin, DeleteView):
    model = Grado
    template_name = 'notas/grados/eliminar.html'
    success_url = reverse_lazy('notas:lista_grados')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Grado eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)



#==============================================Materias========================================================
#--------------------------------------------------------------------------------------------------------------
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


#==============================================Notas===========================================================
#--------------------------------------------------------------------------------------------------------------
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


#==============================================Informes finales================================================
#--------------------------------------------------------------------------------------------------------------
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



#==============================================Estadísticas========================================================
#------------------------------------------------------------------------------------------------------------------


