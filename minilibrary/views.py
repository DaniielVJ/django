import time
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.urls import reverse_lazy
# Poder hacer condiciones con operadores logicos en los filtros
from django.db.models import Q
# Importamos el Paginador del modulo paginator, que incluye todas las funcionalidades para implementar un paginador
from django.core.paginator import Paginator # Gestiona todos los objetos Page que tienen la divison de objetos
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
# Este decorador lo importamos, para aplicarlos a las view, que necesiten login o autenticacion 
from django.contrib.auth.decorators import login_required, permission_required
# Esta clase la importamos, para aplicarla a las view class que requieren login antes de usarse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


from .utils import funciones
from .models import Book, Review
from .forms import ReviewSimpleForm, ReviewModelForm, BookForm


User = get_user_model()

# Function-Based View
def hello_fbv(request):
    return HttpResponse("Saludos desde una view basada en funciones")

# Class-Based View
class HelloCBV(View):
    # View es la base de las CBV asi que no le sobreescribimos los metodos get, post, put, etc. ya que esta
    # no los implementa solo se encarga de crear la logica para pasarle el request correspondiente a esos metodos
    # si fuera una clase que hereda de View como las genericas o mixins esas si le sobreescribimos sus metodos
    # la cosa es que podemos crear metodos con todos estos nombres para utilizar en nuestra CBV que View enrutara la request:
    """
    http_method_names = [
        "get",
        "post",
        "put",
        "patch",
        "delete",
        "head",
        "options",
        "trace",
    """
    def get(self, request, *args, **kwargs):
        return HttpResponse("Saludos desde una view basada en clases")
        

# Ahora esta view requiere login, colocamos loginrequiredmixin para que tenga prioridad de las demas clases
# y ninguna pueda sobreescribir su dispatch, que se encarga de solicitar Login, tampoco nosotros :v solo si sabemos lo que hacemos.
class WelcomeView(LoginRequiredMixin, TemplateView):
    # sobreescribimos este atributo, con el nombre del template que debe renderizar
    # esta view cuando una url lo mande a llamar porque recibio un request http get
    template_name = "minilibrary/welcome.html"

    # sobreescribimos este metodo que implementa TemplateView y heredamos
    def get_context_data(self, **kwargs):
        # aqui recibimos el contexto que ya implementa TemplateView para el template
        context = super().get_context_data(**kwargs)
        # y aparte a los datos que ya implementa TemplateView añadir los nuestros
        # es decir los que queremos pasar nosotros al template para usarlos ahi

        # Aqui añadimos nuestros datos al contexto que es un diccionario con los que ya implementa 
        # django para el template
        context['total_books'] = Book.objects.count()
        return context # lo que retorna este metodo django lo carga como contexto a los templates
    
        # tener cuidado ajajjaa, de sobreescribir una key que ya implemente django como "view" que este la añade
        # el get_context_data que heredamos y le da como valor la instancia misma de WelcomeView
        
# Para no implementar Logica desde cero con View, vamos a reutilizar ListView
class BookListView(ListView):
    # atributo que indica a la View de que modelo debe listar los objetos
    model = Book
    # Especificamos que template debe pasar el contexto o los objetos que queremos renderizar
    template_name = "minilibrary/books.html"
    # Si no se especifica el template donde se pasaran los objetos a listar, por defecto django busca en la carpeta
    # de la app en templates un template que se llame como el modelo_list.html Ej: para esta app buscaria en templates
    # carpeta llamada minilibrary un template book_list.html y a ese pasaria los objetos.
    
    # especificamos con que nombre se enviaran los objetos al template
    context_object_name = "books" # cuando no lo asignamos el nombre por defecto es model_list, ej: book_list

    # indicamos que queremos los objetos paginados, e indicamos el numero de paginas
    paginate_by = 5 # el object name books se pasara solo con 5 objetos pq es la pagina

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        last_viewed_book = self.request.session.get('last_viewed_book')
        kwargs['last_book'] = self.model.objects.get(pk=last_viewed_book) if  last_viewed_book else ''
        return kwargs



# Para no implementar Logica desde cero con View, vamos a reutilizar DetailView
class BookDetailView(LoginRequiredMixin, DetailView):
    # Especificar de que modelo obtendra el objeto la view
    model = Book
    # Indicar que template se va a renderizar con los detalles del objeto
    template_name = "minilibrary/detail_book.html"
    # Indicar el nombre con el que indentificaremos al objeto dentro del template
    context_object_name = "book"
    # Si usamos slug en vez de el id o primary key para buscar el objeto debemos
    # indicar el nombre del campo del modelo que contiene el slug
    slug_field = "slug"
    slug_url_kwarg = "slug"
    # ERROR 404 se manda automaticamente el template 404.html si no se encuentra el recurso
    # al cual se esta consultando en el request a la url

    # Sobreescribimos el metodo get que implementa por defecto la DetailView
    def get(self, request, *args, **kwargs):
        if request.user.has_perm('minilibrary.view_book'):
            response = super().get(request, *args, **kwargs)
            request.session['last_viewed_book'] = self.object.id
            return response
        else:
            return HttpResponseForbidden("No tienes permiso para ver los detalles de un libro")



# Para no implementar Logica desde cero con View, vamos a reutilizar y extender CreateView
class ReviewCreateView(CreateView):
    # Especificar el modelo donde se almacenara el objeto
    model = Review
    # Atributo que usa CreateView para definir que formulario usara para obtener los datos del objeto a crear
    form_class = ReviewModelForm
    # Indicamos el template HTML donde se renderizara el formulario para obtener los datos del objeto a crear
    # en el template se pasa en el context el formulario con el nombre de form, para referenciarlo en el context del template
    template_name = "minilibrary/add_review2.html"


    # Este metodo definimos toda la logica que ejecutara la view si los datos proporcionados al formulario son validos, es decir .is_valid() es True
    def form_valid(self, form):
        # por defecto si no sobreescribimos el form_valid del padre este creara una instancia del modelo la almacenara
        # en la tabla del modelo y asignara la intancia a self.object y retornara lo que retorna su metodo padre
        # es un HttpResponseRedirect a la success_url que se especifique. asi que si no lo sobrescribimos automaticamente
        # almacena el objeto y lo redirecciona a la url que le pasemos en success_url a la clase.
        # Ahora saber esta información igual es util por si queremos utilizar el form_valid del padre dentro de nuestro
        # form_valid que estamos sobrescribiendo, o simplemente no llamarlo y que nuestra view ejecute su propia logica 
        # y redireccione o haga lo que quiera. 
        # Esto es fundamental ya que podemos manipular la instancia que creamos a partir de los datos del formulario
        # como por ejemplo aqui aun esta incompleta le falta que le asignemos el book y user al cual esta asociada la review
        # asi que podemos asignarcelos y luego pasar el formulario al form_valid del padre para que haga la tarea por defecto
        # que es almacenar el objeto en el Modelo.
        
        # El atributo kwargs de nuestra view contiene los valores que se envian en los parametros de las urls dinamicas
        book_id = self.kwargs.get("pk")
        # Obtengo el objeto o libro del modelo al cual asociaremos a este objeto review
        book = get_object_or_404(Book, pk=book_id)
        # Obtenemos el usuario que envio el request con los datos del formulario para asociarle a el la review
        # ya que el la esta agregando
        user = self.request.user if self.request.user.is_authenticated else User.objects.first()

        # Aqui podemos usar el atributo instance para obtener el objeto o review que estamos creando o se almacenara
        # ya que despues de que se valida el formulario .is_valid() a la instancia de form.instance se le rellena con los datos
        # validados o cleaned, antes de validar esta la instancia vacia.
        review = form.instance

        # asignamos los datos faltantes a la review
        review.book = book
        # asociamos la review al usuario que relleno el formulario y mando el request
        review.user = user
        print("MISMOS OBJETOS: ", review is form.instance)
        # cargamos mensajes de success para el siguiente render si es que se almacena correctamente
        messages.success(self.request, "Review añadida exitosamente")

        # Aqui se espera una respuesta HTTP para enviar el usuario, esta la retorna el form_valid del padre y ademas este
        # almacena la instance del formulario en el modelo, da igual si aqui le asignamos los valores con review ya que
        # al asignarle a la variable review la referencia de form.instance ambos apuntan al mismo objeto que es el almacena
        # en el modelo la View de django.
        return super().form_valid(form)


    def form_invalid(self, form):
        messages.error(self.request, "Datos invalidos", "danger")
        return super().form_invalid(form)
    
    # Este metodo es el que usa una View para obtener la url donde se redireccionara al usuario luego
    # que registre el objeto o review exitosamente en el modelo
    def get_success_url(self):
        # usamos reverse_lazy o peresoso que permite obtener la url o path completo de una url por su nombre
        # y luego en su parametro kwargs pasamos todos los parametros y valores que pasaremos a esos parametros
        # de la url si es una url dinamica.
        return reverse_lazy('book_detail', kwargs={"pk": self.kwargs.get("pk")})
    

    # Modificamos el que como obtendra el formulario la view antes de que lo valide, ya que debemos al formulario que crea con los datos
    # enviados por el request a su metodo post() añadirle como atributo el request, ya que la clase que usamos para definir el formulario
    # modificamos su codigo interno de su constructor, y clean que ocupan el request, asi que debemos pasarselo en el atributo
    def get_form(self, form_class = None):
        form = super().get_form(form_class)
        form.request = self.request
        return form

# class-based view que implementa la logica para actualizar los datos de un objeto existente: UpdateView
class ReviewUpdateView(UpdateView):
    # extendemos para nuestro caso de uso
    model = Review
    form_class = ReviewModelForm
    # reutilizamos el template, ya que este renderiza el formulario para ingresar los datos de rating y text
    # que son los mismos que necesitaremos para actualizar la review
    template_name = "minilibrary/add_review2.html"

    def get_form(self, form_class = None):
        form =  super().get_form(form_class)
        form.request = self.request
        return form

    # por defecto usa el get_queryset de todas las view genericas, que devuelve todos los objetos del modelo, pero internamente
    # UpdateView implementa la logica para obtener solo el objeto que tenga como pk o id o slug el valor que se envia por la url
    # a alguno de esos parametros (pk, id, slug) y entonces el sabe que ese objeto que tenga es el que debe actualizar, entonces
    # si se recibe un request con metodo get carga todos esos datos en el formulario para que se renderize con los datos que ya
    # se tienen para el objeto a editar en la DB, si recibe request metodo POST simplemente va a buscar el objeto para rellenar
    # el formulario en los campos que no se proporciono datos por el usuario los valores que ya tenia el objeto para que cuando se haga .save
    # como ya existe se actualizen solo los datos que sean distintos
    def get_queryset(self):
        queryset =  super().get_queryset()
        # porque no get ? pq esto si o si debe devolver un queryset jajaja o si no la view que implementa este metodo podria aplicar
        # un metodo que solo tienen los queryset si uso get ahora obtenemos el objeto luego el afuera aplicara get pensando que es un queryset
        # ya que asi se llama el metodo y abra error que no se encuentra ese metodo definido en el objeto
        queryset =  queryset.filter(user__id=self.request.user.pk) 
        # retornamos un queryset solamente con las review asociadas a ese usuario y que nuestra vista solo puede devolver una review
        # asociada al usuario, esto es muy importante en seguridad pq si no cualquier usuario autenticado en el sistema, podria
        # mandar el id de otra review que no sea de el y si por defecto UpdateView obtiene la review del id que se manda por url
        # podria obtener la de otro usuario, pero si le devolvemos un queryset con solo las que estan asociadas a el, si aplica .get
        # UpdateView al queryset dara un 404 ya que el id que mando el usuario es de una review que o le pertenece y el queryset
        # solo tiene las de el :v asi no nos vulnera si sabe modificar el valor que identifica la review que se quiere actualizar
        # en la url.
        return queryset
    
    

    # Como la UpdateView hace la operación de actualizar los datos de un objeto del modelo review
    # no es necesario especificar a que book o autor hay que asociar esta review pq esta ya al momento que se crea
    # se asocio a un libro y autor, updateview automaticamente los datos que no hayan sido proporcionados por el usuario
    # en el formulario, los rellena con el valor actual que tiene el objeto para esos campos. entonces como solamente
    # obtenemos el rating y text del usuario el form se le actualizan solo esos campos y a los demas los rellena con los datos
    # que ya tenia en la base de datos.
    def form_valid(self, form):
        messages.success(self.request, "Review actualizada correctamente")
        return super().form_valid(form) # este devuelve la redireccion a la url del metodo get_success_url
    
    # Logica que se ejecuta en caso de que los datos que se envian al formulario para actualizar el objeto no sean validos
    def form_invalid(self, form):
        messages.error(self.request, "Datos invalidos")
        return super().form_invalid(form)

    # Lo que retorne este metodo es la url que usara la View para redireccionar al usuario si actualizo correctamente
    def get_success_url(self):
        queryset = self.get_queryset().select_related("book")
        review = get_object_or_404(queryset, pk=self.kwargs.get('pk'))
        # la url a la cual redireccionara al usuario sera a la book_detail y esta recibe el id del libro del cual mostrar sus detalles
        # para eso le pasamos el id del libro al cual esta asociado el review entonces lo devuelve al libro
        return reverse_lazy('book_detail', kwargs={'pk': review.book.id}) # /minilibrary/books/9/ | 9 = <int:pk>
        # esa era mi version para devolver la url que debe redireccionar pq no sabia pero aqui si se peude acceder a la instancia
        # que se queire actualizar con self.object.book.id

        # otra forma es en el modelo de cada instancia o objeto de este modelo tenga un metodo get_absolute_url que permita obtener su url
        # con un return reversed('book_detail', kwargs={'pk': self.pk})

# class-based view que implementa la logica para eliminar un objeto de un modelo en especifico
class ReviewDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    # definimos el modelo del cual eliminara un objeto la DeleteView
    model = Review
    # Este template es el que envia como respuesta si recibe la view un http request GET de que se quiere eliminar un objeto
    template_name = "minilibrary/review_confirm_delete.html"
    # url a la que se redireccionara si se elimina con exito el objeto que solicita el usuario
    success_url = reverse_lazy('list_books')

    # Definimos que permiso debe tener un usuario para poder ejecutar esta class view, multiples permisos se pasan en una tuple
    permission_required = 'minilibrary.delete_review' 

    raise_exception = True

    
    # Se encarga de pasar el queryset a la view, donde el buscara el objeto a eliminar
    def get_queryset(self):
        # No regresamos para que busque en todas las reviews, si no solo en las reviews que esten asociadas al usuario
        # que tenga como id el mismo id del usuario que mando el request
        return super().get_queryset().filter(user__id=self.request.user.pk)
    
    # Este es el metodo que manda a llamar la view cuando recibe un http request POST con el id del objeto a eliminar
    def delete(self, request, *args, **kwargs):
        # cargamos un mensaje en el sistema para que en el siguiente render se muestre, el siguiente render es es la pagina
        # de todos los libros success url.
        messages.success(self.request, "Tu review fue eliminada")

        # El metodo delete del padre o por defecto obtiene la instancia get_object a eliminar obtiene la sucess url
        # con get_succes_url y luego elimina la instancia o objeto que quiere eliminar el usuario pasandolo al metodo .delete()
        # que implementan loso objetos de un modelo (Model), entonces es eliminada en la base de datos y luego retorna una redireccion
        # a la sucess url que definimos y este delete retornara el response a la sucess.url
        return super().delete(request, *args, **kwargs)



@login_required
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

@login_required
@permission_required(['minilibrary.add_review'])
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # debe ser un None, no puede ser un string vacio lo que le mandemos
    form = ReviewModelForm(request, request.POST if request.POST else None)

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
        print(form.is_valid())
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
            # Recordar que la view retorne lo que retorna redirect, ya que este retorna un HttpResponseRedirect que es la respuesta
            # http que la view debe responder todo lo que retorna la view se manda como respuesta al cliente.
            return redirect('add_review', book_id=book.id)
        else:
            messages.error(request, 'Proporciona los datos correctos de los campos del formulario', "danger")
    return render(request, 'minilibrary/add_review2.html', {'form': form, 'book': book})



# View que vinculamos a url, para consultar desde el navegador y probar que el middleware calcule cuanto tiempo tarda
# en regresarle el response despues de haberle pasado el request que se le envio.
def time_test(request):
    # sleep(segundos), bloquea la ejecución del hilo por los segundos que nosotros le proporcionemos
    time.sleep(2)
    return HttpResponse("<h1>View Time Test</h1>")

# View que recibe un request y lee si tiene una sesion activa o le crea una 
def visit_counter(request):
    # django siempre crea una session en memoria para todos los requests que recibe de un navegador, pero no la registra
    # en la base de datos ni la envia como cookie al usuario o navegador hasta que no se escriban datos en ella
    # por lo tanto aqui accedemos a la seccion que se crea para un request y vemos si es que tiene datos escritos en ella
    # visitas, ya que en el codigo la manejamos como diccionario, si no tiene valor retornamos 0 y le escribimos la llave visitas
    # con ese valor, al escribirle valor django ahora esa session sabe que tiene que registrarla pq tenemos datos asociados
    # a ese navegador y ahora debemos hacer una trazabiliad o seguimiento a ese navegador usando la session. 
    visits = request.session.get('visitas', 0)
    visits += 1
    request.session['visitas'] = visits

    # Este metodo permite establecer una expiracion a una sesion en especifico que ejecute esta view, es decir
    # todas las sessiones que ejecutan la view solo duraran 600 segundos activas y luego expiraran.
    request.session.set_expiry(600)
    # valores que puede recibir:
    # 600 -> 10 min, ;  0 -> Al cerrar el navegador -> ; None -> duracion por defecto
    return HttpResponse(f"Has visitado esta pagina {visits} veces")



# view para añadir un libro
def add_book(request):
    if request.method == 'POST':
        # Instanciamos el formulario, y lo rellenamos con los datos y archivos que se enviaron
        form = BookForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book add succesfully')
            return redirect('list_books')
        messages.error(request, form.errors, 'danger')
    else:
        form = BookForm()
    return render(request, 'minilibrary/add_book.html', {'form': form})


