from django.shortcuts import render
from django.http import Http404
from .models import Book
# Poder hacer condiciones con operadores logicos en los filtros
from django.db.models import Q
# Importamos el Paginador del modulo paginator, que incluye todas las funcionalidades para implementar un paginador
from django.core.paginator import Paginator # Gestiona todos los objetos Page que tienen la divison de objetos
from .utils import funciones

# Create your views here.
def index(request):
    try:
        # Cuando se ejecute la url minilibrary/ o se acceda a ella, iremos a buscar todos los libros
        # a la tabla del modelo Book para mostrarcelos al usuario
        books = Book.objects.all()
        
        # Capturamos un valor del formulario si es que el usuario envia uno
        query_search = request.GET.get('query_search')
        
        # Recibimos el rango de fechas por las que desea filtrar el usuario y la formateamos a objetos
        # date de python para manipular  y filtrar
        start_date = funciones.formateador_fecha(request.GET.get("start"))
        end_date = funciones.formateador_fecha(request.GET.get("end"))
        
        if start_date:
            # Filtra o regresa todos los libros que su fecha de publicacion sea igual o mayor
            # a la fecha de inicio especificada
            books = books.filter(publication_date__gte=start_date)
        
        if end_date:
            # Aqui filtramos solo los libros que son de la fecha de start hacia adelante, porque
            # lo estamos aplicando despues del filtro anterior, entonces ahora podemos indicar una fecha termino o fin
            # que debe estar el libro
            books = books.filter(publication_date__lte=end_date)
        
        print(books)

        
        # Si envia un valor filtramos, si no envia nada por el formulario mostramos todos los libros
        if query_search:
            # actualizamos la variable para que tenga el valor que ya tiene anteriormente pero filtrado
            # asi se enviara al template solo los libros que cumplen el filtro del usuario para mostrar
            books = books.filter(Q(title__icontains=query_search) | Q(author__name=query_search))
            # en filter se pasan las condiciones que los objetos del modelo o tabla deben cumplir para traerlos
            # si establecemos varias condiciones por defecto los objetos deben cumplirlas todas a excepcion que usemos
            # operaciones logicas como or not y and usando Q objects.
        
        
        # Creamos el paginador - argumentos
        # 1. queryset que queremos que divida
        # 2. pasar cuantos objetos tendra cada Page() del paginador
        paginator = Paginator(books, 5) # Dividimos en paginas de 5 objetos
        
        # Esta variable obtiene el numero de pagina que quiere cargar el usuario desde el template
        # en el paginador
        # La pagina que queremos que muestre la obtendremos del request, es decir el usuario
        page_number = request.GET.get("page") 
    
        

        # Pasamos el numero de pagina al Paginador para que nos regrese esa Page()
        # y esa enviemos en el template para mostrarle al usuario en el navegador
        page_books = paginator.get_page(page_number)
        
        # page es un objeto que almacena un numero de objetos determinado
        # en este caso el paginador se encargo de definir cuantos objetos tendra cada page
        
        # Lo bueno de usar un paginador en vez de nosotros crear nuestros propios objetos page
        # y mandarcelos al usuario, es que el gestiona todo, como los errores y crear las paginas
        # en pequeños grupos que indiquemos
        
        
        return render(request, 'minilibrary/index.html', {
            # Mandamos los libros paginados o la pagina con los libros
            'page_books': page_books,
            'query_search': query_search,
            
        })
    except Exception:
        # Esta excepcion si queremos que la capture el gestor o capturador de excepciones de django
        # ya que esta programado que cuando sea una excepcion Http404() retornara el template 404.html
        raise Http404()
