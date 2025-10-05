from django.shortcuts import render
from datetime import date


# Create your views here.

def home(request):
    # Devuelve la fecha actual
    today=date.today()
    stack=['Python', 'Django', 'Linux', 'Cloud', 'Docker', 'SQL', 'Routing & Switching']
    # stack=[]
    # Aqui enviamos como respuesta el renderizado de la plantilla html
    return render(request, 'landing/home.html', {"name":"Pedro", "age": 26, 'today': today, 'stack':stack})

