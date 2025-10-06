from django.shortcuts import render
from django.http import HttpResponse
from datetime import date


# Create your views here.

def home(request):
    text="soy un texto CUALQUIERA"
    # Devuelve la fecha actual
    today=date.today()
    stack=[
        {"id": "django", "name":"Django"}, 
        {"id": "linux", "name":"Linux"}, 
        {"id": "docker", "name":"Docker"},
        {"id": "sql", "name":"SQL"}
        ]
    
    # stack=[]
    # Aqui enviamos como respuesta el renderizado de la plantilla html
    return render(request, 'landing/home.html', {"name":"Daniel", "age": 26, 'today': today, 'stack':stack, 'text': text})



def stack_detail(request, tool):
    return HttpResponse(f"Tecnología: {tool}")