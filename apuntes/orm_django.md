Para el orm de django es tal cual esta regla
- Clase == Tabla 
- Atributo == Campo o Columna
- Instancia == Fila o Registro

Eso significa que si queremos crear un registro en una tabla debemos usar la clase que representa esa tabla
```
mi_autor=Author.objects.create(name="Daniel Valdebenito", birth_day='1998-12-30')
```
Creamos un registro o fila en la tabla Author usando su clase correspondiente, y ademas esto nos regresa
una instancia que hace referencia al registro o fila que acabamos de crear y podemos operar sobre esa fila
usando esta instancia. por ejemplo pasandola como valor de un atributo o columna de otro registro que creemos
para indicar que ese registro apunta a ese de la instancia.


```
Book.objects.create(title="Libro fictisio", publication_date='2020-12-12'), author=mi_autor, pages=300, isbn='99999999-9')

```

Simplemente pasamos la instancia con la cual queremos relacionar esta fila que estamos creando y de forma automatica el orm
añadira el id de la fila que representa esa instancia mi_autor en el campo author_id del registro de la otra tabla book.

**python3 manage.py shell** permite ejecutar una shell interactiva en nuestro proyecto django que puede importar modulos o clases de nuestro proyecto. ideal para poder probar nuestros modelos sin necesidad de asignarlos en una vista y acceder a una url para poder ejecutarlo y probarlo. solo importamos nuestros modelos y podemos usarlos. from minilibrary.models import Author, Book

```
# Trae todos los registros de la tabla
Book.objects.all() # Devuelve un iterable donde cada elemento es un objeto del tipo Book que representa una fila en la tabla
```
```
# Trae un iterable con todos los registros que coinciden con el filtro
Book.objects.filter(author__name="Daniel Valdebenito")
```


