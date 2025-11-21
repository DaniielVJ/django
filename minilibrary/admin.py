from django.contrib import admin
# Primero debemos importar los modelos que queremos registrar
from .models import Book, BookDetail, Author, Genre, Recommendation, Review, Loan
# UserAdmin es la que se encarga de personalizar como se va a ver y hacer con el Modelo Users en el django admin
from django.contrib.auth.admin import UserAdmin

# Crear Actions - Funciones que actuan sobre un conjunto de objetos seleccionados desde el admin
@admin.action(description="Marcar devuelto")
def mark_loan_as_returned(model_admin, request, queryset):
    # parametro queryset almacena el queryset con los objetos
    # seleccionados en el admin para aplicar el action
    queryset.filter(is_returned=False).update(is_returned=True)


@admin.action(description="Mostrar fecha de entrega")
def show_return_date(model_admin, request, queryset):
    model_admin.list_display.append('return_date')



# Crear un inline de tipo tabular
class ReviewInline(admin.TabularInline):
    # Indicamos de que modelo es este inline (El que tien el campo foreign o OneToOne)
    model = Review
    extra = 1

    # Una vez creado se asocia al modelo que queramos que pueda editar o acceder
    # a los objetos del modelo de este inline

# Crear un inline de tipo stack
class BookInline(admin.StackedInline): # Creamos un inline para el modelo book
    # especificamos que es para el modelo book
    model = Book 
    # cuantos formularios vacios agregaremos para añadir book desde los modelos que 
    # vinculemos el inline
    extra = 1

class BookDetailInline(admin.StackedInline):
    model = BookDetail
    # cuando el inline se agregue a un modelo solo se agregara un formulario vacio
    extra = 1
    # Nombre con el que se identificara este inline dentro del admin
    verbose_name_plural = 'Detalles de Libro'
    verbose_name = 'Detalle del Libro'

class LoanInline(admin.TabularInline):
    model = Loan
    extra = 1
    verbose_name_plural = 'Prestamos'


# Añadimos inline a un modelo que ya existe y ya registro django
UserAdmin.inlines = (LoanInline, )


# Podemos usar un decorador para registrar y configurar un modelo en el admin a la vez
@admin.register(Book)
# Con esta clase personalizamos lo que podemos con el modelo desde el admin
class BookAdmin(admin.ModelAdmin): # Debe heredar de ModelAdmin, convencion tenga el nombre del modelo que queremos personalizar
    # Aqui modificamos los atributos que ofrece ModelAdmin, para indicar
    # que podra hacer el admin con cada modelo, PODEMOS USAR LISTAS O TUPLAS

    # Especifica que campos se mostraran en el admin al visualizar todos los objetos del modelo
    list_display =  ('title', 'author__name', 'publication_date', 'isbn', 'pages')
    # Especificamos porque campos podremos hacer busquedas de los objetos del modelo en el admin
    search_fields = ('title', 'author__name')
    
    # Recordar que cuando manipulamos un campo de tipo ForeignKey, con el doble guion bajo podemos
    # especificar un campo del objeto asociado.

    # Añadir filtros al modelo en el admin
    list_filter = ('author__name', 'genres__name', 'publication_date') # Si un Libro tiene un autor con ese nombre lo muestra o genero

    # Especificar porque campos podemos ordenar los objetos del modelo (El menos - , es forma descendente mas actual mas antiguo)
    ordering = ('-publication_date', ) 
    
    # Añade una navegacion por años para filtrar en los objetos del modelo en el admin
    date_hierarchy = 'publication_date' # Por defecto carga todos los años que aparecen en el modelo EJ: Si no hay un objeto con el año 2025, no aparece ese año en el filtro

    # Asociamos inline, permitiendo que desde el menu de los objetos de este modelo podamos editar
    inlines = (ReviewInline, BookDetailInline)

    # Crear fieldset en los formularios para cada grupo de campo a modificar, agregar, eliminar en el admin
    fieldsets = (
        # Cada tupla es un fieldset que agrupa campos para un objeto o modelo
        ('Información general', { "fields": ('title', 'author', 'publication_date', 'genres') }),
        ('Mas información', {"fields": ('isbn', 'pages')}),
    )

    # Una vez especificado los campos con autocompletado, se debe especificar en sus modeladmin, cuales
    # seran los campos de busqueda por los cuales se hara el autocompletado
    autocomplete_fields = ['author', 'genres']

    # Sobreescribimos metodos

    # Este metodo sirve para indicar si el usuario puede añadir permisos
    # aqui retornamos que si el usuario del que interactua con el servidor o backend envia request
    # es superuser puede hacerlo. añadir permisos
    def has_add_permission(self, request):
        return request.user.is_superuser
    
    # Estos metodos sirven para indicar si el que envio el request puede ejecutar tareas de añadir o modificar permisos
    # si retornan True los que manden request pueden realizar esas acciones por eso debemos hacer evaluaciones antes
    # de retornar True en este caso se retorna True si tienen habilitado is_superuser o is_staff
    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    
    # Literalmente el tipo de usuario que retornemos se le otorgan esos permisos.
    
    # Los permisos de codigo tiene prioridad sobre los de el admin, ya que estos sirven para proteger el modelo
    # indicando que tipo de usuario puede hacer que cosa, y aunque este en un grupo que le de el permiso de agregar
    # aqui estamos protegiendo que solo puede hacerlo el superuusario asi que no tendra la opcion.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    inlines = (BookInline, )
    # Esto indica que el campo con autocompletado buscara por el nombre del autor 
    # o autocompletara por el nombre
    search_fields = ('name', )

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name', )

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['user__username', 'book__title', 'is_returned', 'loan_date']
    # Establecer campos de solo lectura, el usuario no podra modificar desde el admin
    readonly_fields = ('loan_date',) 
    actions = (mark_loan_as_returned, show_return_date)
    raw_id_fields = ('user', 'book')
    





# Aqui registramos los modelos
# admin.site.register(Author)
# Para usar las configuraciones personalizadas, debemos registrarlas junto a su modelo
# admin.site.register(Book, BookAdmin)
admin.site.register(BookDetail)
# admin.site.register(Genre)
admin.site.register(Recommendation)
admin.site.register(Review)
# admin.site.register(Loan)



