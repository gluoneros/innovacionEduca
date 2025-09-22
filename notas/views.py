from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import EscalaNota, AnioEscolar, Grado, Materia, Periodo, Nota, InformeFinal
from .forms import (
    EscalaNotaForm, AnioEscolarForm, GradoForm, MateriaForm, 
    PeriodoForm, NotaForm, InformeFinalForm, BuscarEstudianteForm, 
    BuscarNotaForm, ImportarNotasForm
)


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