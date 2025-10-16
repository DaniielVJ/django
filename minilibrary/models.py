from django.db import models

# Aqui creamos los modelos que representan las tablas de la base de datos
# Cada clase es una tabla en el ORM

 # Esta clase sera mi tabla autor en la base de datos, porque hereda de models.Model
class Author(models.Model):
    # Cada atributo definido en la clase, va a ser una columna en la tabla
    name = models.CharField(max_length=100, null=False) # Indicamos de que tipo de campo sera nuestra columna
    # Nuestra columna name sera un campo de texto con una longitud maxima de 100 caracteres 
    # El parametro es para indicar si el campo aceptara nulos o no en la tabla
    birth_day = models.DateField(null=True, blank=True)



# Esta clase es un modelo, porque hereda de Model, por ende indicamos a django que esta clase representa a una tabla
# En la base de datos que se llama Book
class Book(models.Model):
    # 1. Cada atributo de una clase Model representa a una columna de la tabla
    # 2. Se le asigna que tipo de campo es esa columna y que configuraciones tiene o tendra.
    
    title = models.CharField(max_length=200)
    publication_date = models.DateField(null=True, blank=True)
    # related_name es un atributo que definira django orm, para usar en la tabla a la cual hace referencia
    # esta foreignkey, para acceder a todos los registros que tiene asociados con esta tabla, es decir
    # podremos desde autor acceder a los libros que tiene asociado.
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    pages = models.IntegerField()
    isbn = models.CharField(max_length=100) 
    
'''
Por ende los modelos es una abstraccion completa de la base de datos en nuestra aplicacion
Donde cada clase representa a una tabla en la base de datos, sus atributos las columnas y cada objeto una fila en la tabla
El ORM de Django es luego el encargado de leer estas clases y migrarlas a tablas en la base de datos e igualmente el encargado
de proveer funcionalidades a estas clases para interactuar sobre la tabla que representan. permitiendonos acceder a sus datos
a traves de metodos en vez de SQL.
'''