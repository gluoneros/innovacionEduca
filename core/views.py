from django.shortcuts import render

def landing(request):
    return render(request, 'core/landing.html')

def error_404_view(request, exception):
    return render(request, 'core/404.html', status=404)