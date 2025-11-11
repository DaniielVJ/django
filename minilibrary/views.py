from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
# Poder hacer condiciones con operadores logicos en los filtros
from django.db.models import Q
# Importamos el Paginador del modulo paginator, que incluye todas las funcionalidades para implementar un paginador
from django.core.paginator import Paginator # Gestiona todos los objetos Page que tienen la divison de objetos
from django.contrib.auth import get_user_model
from django.contrib import messages
from .utils import funciones
from .models import Book, Review
from .forms import ReviewSimpleForm, ReviewModelForm

User = get_user_model()

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
        
        # generamos una copia del diccionario
        query_params = request.GET.copy()
        
        # Eliminamos el parametro de page en nuestro query params porque no lo necesitamos
        # aparte esa info de la pagina la maneja el paginador
        if "page" in query_params:
            query_params.pop("page")
        
        # Este metodo django se lo agrega a los diccionarios, para convertir todos los parametros que
        # recibimos por GET que ahora estan en un diccionario en una url
        query_string = query_params.urlencode() 
        # Esto significa que en vez de que cada elemento sea en este formato -> key:value,key2:value 
        # se vera -> key=value&key2=value en un string
        
        
        # page es un objeto que almacena un numero de objetos determinado
        # en este caso el paginador se encargo de definir cuantos objetos tendra cada page
        
        # Lo bueno de usar un paginador en vez de nosotros crear nuestros propios objetos page
        # y mandarcelos al usuario, es que el gestiona todo, como los errores y crear las paginas
        # en pequeños grupos que indiquemos
        
        
        return render(request, 'minilibrary/index.html', {
            # Mandamos los libros paginados o la pagina con los libros
            'page_books': page_books,
            'query_search': query_search,
            'query_string': query_string,
            
        })
    except Exception:
        # Esta excepcion si queremos que la capture el gestor o capturador de excepciones de django
        # ya que esta programado que cuando sea una excepcion Http404() retornara el template 404.html
        raise Http404()



def recomendar_libro(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    form = ReviewSimpleForm(request.POST or None)    

    
    if request.method == 'POST':
        if form.is_valid():
            rating = form.cleaned_data["rating"]
            text = form.cleaned_data["text"]
            user = request.user if request.user.is_authenticated else User.objects.first()
            Review.objects.get_or_create(user=user, book=book, rating=rating, text=text)
            
            messages.success(request, 'Review creada con exito')
            # Los rederict por defecto son con metodo GET, significa que envian un request a la url que le pasemos
            # y el segundo argumento pasamos parametros que se puedan enviar en a esa url si esta es dinamica y acepta eso
            return redirect("recomendar_libro", book_id=book_id)
        else:
            messages.error(request, "Corrige los errores del formulario")
    return render(request, 'minilibrary/add_review.html', {'form': form, 'book': book})


    
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    form = ReviewModelForm(request.POST or None)

    # form implementa iter, asi que podemos iterarlo, donde cada elemento es un field o campo del formulario
    # en su formato html,  form.visible_fields() -> trae los campos visibles solamente que son los que se mostraran en el html
    for field in form:
        # son objetos pero al imprimirlos se muestra su forma en html
        # acceder al texto que se muestra del campo en el html
        print(field.label)
        # regresa el html del label completo
        print(field.label_tag())
        # acceder al campo en si, el input en formato html
        print(field) # su version imprimible es un string con el html

    if request.method == 'POST':
        
        if form.is_valid():
            # commit False, permite que en vez de crear un objeto del modelo y guardarlo en su tabla, simplemente
            # nos regrese el objeto del modelo con los campos que tengan valor.
            review = form.save(commit=False)
            # Al objeto del modelo review, que es la review indicamos el libro al cual esta asocida
            review.book = book
            # Indicamos el usuario que hizo la review (el que mando el request y esta autenticado)
            review.user = request.user if request.user.is_authenticated else User.objects.first()
            # Almacenamos la review en la tabla de su modelo Review
            review.save()
            messages.success(request, 'Review añadida exitosamente')
            redirect('add_review', book_id=book.id)
        else:
            messages.error(request, 'Proporciona los datos correctos de los campos del formulario')
    return render(request, 'minilibrary/add_review2.html', {'form': form, 'book': book})