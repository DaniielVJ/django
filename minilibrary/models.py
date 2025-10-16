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


class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_date = models.DateField(null=True, blank=True)
    # related_name es un atributo que definira django orm, para usar en la tabla a la cual hace referencia
    # esta foreignkey, para acceder a todos los registros que tiene asociados con esta tabla, es decir
    # podremos desde autor acceder a los libros que tiene asociado.
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    pages = models.IntegerField()
    isbn = models.CharField(max_length=100) 