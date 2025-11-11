from django.db import models
from django.contrib.auth import get_user_model

# Obtenemos el modelo que se este usando para los usuarios en el sistema
User = get_user_model()

# Aqui creamos los modelos o clases que representan las tablas de la base de datos
# Cada clase es una tabla en el ORM
class Author(models.Model):
    name = models.CharField(max_length=100, null=False) 
    birth_date = models.DateField(null=True, blank=True)
    
    
    def __str__(self):
        # Permite indicar como se vera cada objeto de una clase en formato de texto
        return f"{self.__class__.__name__}(name={self.name}, birth_day={self.birth_date})"


class Genre(models.Model):
    # no puede haber generos con un name repetido
    name = models.CharField(max_length=50, null=False, unique=True)
    
    class Meta:
        verbose_name = "Genero"
        verbose_name_plural = "Generos"


    def __str__(self):
        return self.name

# Esta clase es un modelo, porque hereda de Model, por ende indicamos a django que esta clase representa a una tabla
# En la base de datos que se llama Book
class Book(models.Model):
    # 1. Cada atributo de una clase Model representa a una columna o campo de la tabla
    # 2. Se le asigna que tipo de campo es esa columna y que configuraciones tiene o tendra.
    
    title = models.CharField(max_length=200)
    publication_date = models.DateField(null=True, blank=True)
    # related_name es un atributo que definira django orm, para usar en la tabla a la cual hace referencia
    # esta foreignkey, para acceder a todos los registros que tiene asociados con esta tabla, es decir
    # podremos desde autor acceder a los libros que tiene asociado.
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    pages = models.IntegerField()
    isbn = models.CharField(max_length=100) 
    # Establecemos este tipo de campo, como el encargado de asociar a cada objeto de este modelo
    # con muchos objetos de otro modelo
    genres = models.ManyToManyField(Genre, related_name="books") # Indicamos con que modelo o tabla es la relacion de mucho a muchos

    # Relacion muchos a muchos pero usando un modelo personalizado como tabla intermedia
    recommendation_by = models.ManyToManyField(User, through="Recommendation", related_name="recommendations")
    
    class Meta:
        # Define con que nombres se mostrara el modelo en el panel web del django admin
        verbose_name = 'Libro' # singular
        verbose_name_plural = 'Libros' 

    def __str__(self):
        return self.title


# Modelo para extender la informacion de el modelo Book
class BookDetail(models.Model):
    # Usamos textfield para ver que sirve para textos largos, pero un charfield largo es mas que suficiente
    summary = models.TextField()
    cover_url = models.CharField()
    language = models.CharField(max_length=60)
    # detail, es el nombre que usaran los objetos del modelo Book para acceder al objeto que tienen 
    # asociado en el modelo bookdetail
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='detail')
    # nombre del atributo que debe usar el libro, para acceder al objeto bookdetail que tiene asociado

    def __str__(self):
        return self.book.title + " Detail"
    
    
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} --> {self.book} ({self.rating}/5)"
    

class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="loans")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans")
    loan_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True, auto_now=True)
    is_returned = models.BooleanField(default=False)
    
    # Usa este enfoque django de clase anidada para aplicar config, por el echo de que
    # debe separar que un atributo es un campo del modelo y otro es de configuracion
    # entonces para eso dice que se metan dentro de una clase Meta, y todo los atributos
    # que esten ahi dentro no los tomara como campos de la tabla si no como configuracion
    class Meta:
        verbose_name = "Prestamo"
        verbose_name_plural = "Prestamos"
    
    
    
    def __str__(self):
        return f"{self.user} ---> {self.book} en {self.loan_date} ({'Devuelto' if self.is_returned else 'Prestado'})"
    
    
# Nosotros definimos un Modelo que sera la tabla intermedia
class Recommendation(models.Model):
    # Una tabla intermedia es una que tiene mas de 1 campo foreignKey
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # La diferencia a otros modelos con mas de 1 campo foreignKey es que aqui no pasamos related_name
    # ya que no queremos que este modelo se comporte como una relacion de 1 a muchos entre los modelos 
    # relacionados. si no que se como una tabla intermedia de una relacion ManyToMany establecida
    # de otro modelo con otro modelo
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    recommended_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)
    
    # una clase anidada como Meta, django la usa para cargar metadatos internos relacionados a la clase
    # como configuraciones de esta. Le dice a django que caracteristica o como debe comportarse la clase 
    class Meta:
        # unique_together se usa para indicar qu eno puede existir mas de una fila o objeto en la tabla
        # que tenga los mismos valores en esos 2 campos a la vez. Esto se traduce a que no puede existir
        # mas de una recomendacion de un usuario para un libro.
        unique_together = ("user", "book")
        # Muy util esa configuracion especial de django, por ejemplo un modelo inscripciones que almacene
        # las inscripciones de un alumno a un curso. por objeto o por inscripcion no debe repetirse
        # el estudiante y curso a la vez ya que un mismo estudiante no debe poder registrarse al mismo curso
        # entonces no puede repetirse esos 2 campos a la vez.

    def __str__(self):
        return f"{self.book} recomendado por {self.user}"

'''

Por ende los modelos es una abstraccion completa de la base de datos en nuestra aplicacion
Donde cada clase representa a una tabla en la base de datos, sus atributos las columnas y cada objeto una fila en la tabla.
El ORM de Django es luego el encargado de leer estas clases y migrarlas a tablas en la base de datos e igualmente es _el encargado
de proveer funcionalidades a estas clases para interactuar sobre la tabla que representan. permitiendonos acceder a sus datos
a traves de metodos en vez de SQL.
'''