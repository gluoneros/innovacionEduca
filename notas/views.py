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
