from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.core.exceptions import ValidationError

from .models import AnioEscolar, Grado, Materia, Periodo, Nota, InformeFinal, EscalaNota
from users.models import Estudiante, Profesor


class AnioEscolarListView(ListView):
    model = AnioEscolar
    template_name = 'notas/anio_list.html'
    context_object_name = 'anios'

class AnioEscolarDetailView(DetailView):
    model = AnioEscolar
    template_name = 'notas/anio_detail.html'
    context_object_name = 'anio'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['periodos'] = self.object.periodos.all()
        context['grados'] = self.object.grados.all()
        return context
    
class PeriodoCreateView(CreateView):
    model = Periodo
    fields = ['nombre', 'porcentaje']
    template_name = 'notas/periodo_form.html'
    
    def form_valid(self, form):
        anio = get_object_or_404(AnioEscolar, pk=self.kwargs['anio_id'])
        form.instance.anio_escolar = anio
        try:
            form.instance.clean()
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('anio_detail', kwargs={'pk': self.kwargs['anio_id']})
    


