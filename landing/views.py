from django.shortcuts import render


# Create your views here.

def home(request):
    # Aqui enviamos como respuesta el renderizado de la plantilla html
    return render(request, 'landing/home.html', {"name":"Daniel"})