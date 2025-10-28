from django.shortcuts import render
from .models import Book
# Poder hacer condiciones con operadores logicos en los filtros
from django.db.models import Q

# Create your views here.
def index(request):
    # Cuando se ejecute la url minilibrary/ o se acceda a ella, iremos a buscar todos los libros
    # a la tabla del modelo Book para mostrarcelos al usuario
    books = Book.objects.all()
    
    # Capturamos un valor del formulario si es que el usuario envia uno
    query_search = request.GET.get('query_search')
    
    # Si envia un valor filtramos, si no envia nada por el formulario mostramos todos los libros
    if query_search:
        # actualizamos la variable para que tenga el valor que ya tiene anteriormente pero filtrado
        # asi se enviara al template solo los libros que cumplen el filtro del usuario para mostrar
        books = books.filter(Q(title__icontains=query_search) | Q(author__name=query_search))
        # en filter se pasan las condiciones que los objetos del modelo o tabla deben cumplir para traerlos
        # si establecemos varias condiciones por defecto los objetos deben cumplirlas todas a excepcion que usemos
        # operaciones logicas como or not y and usando Q objects.
    
    print(query_search)
    return render(request, 'minilibrary/index.html', {
        'books': books,
        'query_search': query_search,
        
    })