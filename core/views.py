from django.shortcuts import render
from django.http import HttpResponseNotFound


def landing(request):
    return render(request, 'core/landing.html')

def page_not_found(request, exception):
    return render(request, 'core/404.html', status=404)
