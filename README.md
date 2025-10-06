## Templates
- Los templates son html que generaremos  para mostrar o presentar los datos al usuario desde el navegador, ya que django a traves de su lenguaje de plantillas (DTL) permite darle esteroides al html y generar interfaces al usuario para que interactuee con la aplicacion, a esta podemos agregarle codigo estatico como css, js, imagenes.

- **Funcion reverse:**  Funcion que permite que obtengamos de forma dinamica la ruta completa de un path a traves de el name que le hayamos otorgado. y si este path tiene partes donde recibe un valor dinamico y no estatico podemos establecer cual es el valor a traves de su parametro args.

- **Crear Templates:** Como buena practica para crear los templates, para cada aplicacion crearemos una carpeta templates y ahi dentro otra carpeta con el nombre de la aplicacion. Dentro de esa ubicacion vamos crear nuestros archivos html que funcionaran como plantillas de nuestra aplicacion.

- **Habilitar los snippets de html para los django templates:** CTRL+SHIFT+P>settings.json>Agregamos la siguiente configuracion:<br>
```    "emmet.includeLanguages": {
        "django-html": "html"
    },
```

- **Registrar los templates:** Para poder utilizar los templates que creemos de nuestra aplicacion, debemos registrarlos en el proyecto en el  modulo settings.py especificando las rutas de las carpetas templates de nuestras aplicaciones.<br>
Podemos registrar las carpetas de forma individual para cada aplicacion:<br>
```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Aqui proporcionamos la ruta absoluta a las carpetas donde se encuentran los templates
        'DIRS': [
            BASE_DIR / "landing" / "templates"
            ],
        # Habilitamos esta opcion como True, para que django cargue los templates de las aplicaciones de forma automatica
        'APP_DIRS': True,
```
<br>
Ahora si tenemos nuestra aplicacion instalada en el proyecto, simplemente teniendo habilitado la opcion APP_DIRS de los templates django buscara los templates de forma automatica en la carpeta templates de nuestras aplicaciones.

- **Renderizar un template:** Renderizar es establecer como se mostrara finalmente el html al usuario, para renderizar un template html usamos de django.shortcuts el metodo render, que es una funcion que le debemos pasar el html que queremos renderizar y esta sera encargada de leer el html o plantilla, ejecutarlo y generar el html resultante que al final sera enviado al usuario.

- **Crear una carpeta con el mismo nombre de la app en la carpeta templates:** Esto se hace para evitar que cuando django cargue todos los templates html del proyecto, no ocurra el problema de que entre aplicaciones existan templates que se llamen igual y se sobreescriban, ya que al hacerlo de esta forma al momento de pasar el template a django este iria con el nombre de la app/template.hmtl-> landing/home.html, quotes/home.html, pero si los ponemos directamente en la carpeta templates el html cargaria dos home.html y no podria diferenciarlos.

- **Interpolacion de valores:** Permite pasar valores o datos de python al template html y cargar esos datos en el documento html para mostrar o presentar al usuario en el navegador.

- **Django templates language:** Es un lenguaje especial que implementa django para poder utilizarlo junto al html template, y es el que nos permitira usar variables y mas cosas de python dentro de un documento html, otorgandole poderes al mismo. ya que de pasar a ser un archivo estatico, a pasar a ser un archivo que genera el contenido html de forma dinamica con los datos obtenidos de python.

- **Enviar valores a un template html:** Para enviar valores al html y usarlos ahi dentro, debemos como tercer parametro a la funcion render pasarle un diccionario, donde cada elemento de este sera un valor de una variable o algo que queremos pasarle al html, el valor que queremos pasar al html se identifica adentro con el nombre de la key que se le asigno en el diccionaro.

```
# Podemos pasar una variable o un valor en codigo duro al html, y lo podremos usar dentro de este con la key que se le asigno
# en este caso name
render(request, 'landing/home.html', {"name":"Daniel"})
```

<br>
e igualmente dentro del html para usar los valores que enviamos de python debemos escribir en el lenguaje de plantillas, para indicar a django que estamos escribiendo en lenguaje de plantillas en vez de html usamos llaves {} y dentro de esta escribimos en el lenguaje de plantillas. ahora los valores de variable se cargan con llaves igualmente dentro de las llaves del lenguaje de plantillas. EJ:<br>

```    
<h2>Hola {{name}}</h2>
```

- **Filtros templates:** Los filtros permiten modificar el como se veran o como se mostraran los valores del template. Para aplicarlos hacemos {{variable | filter1}} o agregar mas filtros {{variable | filter1 | filter2}}. asi podemos modificar o transformar los valores para que se muestren de una forma u otra. 
El filtro permite decorar el como se mostraran los datos

- **Tags:** Son instrucciones que podemos utilizar para implementar una funcionalidad dentro de nuestro html.<br>
Los tags se definen con la sintaxis {% tag argumento %}, algunos solo tienen apertura pero tambien pueden tener cierre EJ:

``` 
{% autoescape  on%}
    {{Aqui se aplica el elemento que sera afectado o se le aplicara la funcionalidad del tag }}
{% endautoescape %}
```
<br> Ejemplo el autoescape es un tag que implementa por defecto django en todos los html y lo que hace es que escapa los caracteres especiales de las variables que pasemos como <> y los remplaza por su codigo en html para que sea interpretado como texto como tal, desactivar el autoescape permite que se implemente el valor de la variable tal cual como lo definimos.
EJ:

```
# Autoescape activado
variable = "<script>alert('Hola')</script>"
# Lo cargaria en el html de esta forma
&lt;script&gt;alert('Hola')&lt;/script&gt; # no se aplicaria el script, si no que se mostraria un texto

# Autoescape desactivado
{% autoescape off %}
# Todo lo que ponemos aqui dentro escapara 
{{variable}} # se agrega tal cual como fue definida, se aplicara el script
{% endautoescape %}

# Evitamos que html escape a los caracteres especiales
```
<br>

- **if tag**

```
    <!--Todo lo que este entre el tag de apertura y cierre se va agregar como parte del html si el argumento
    es True o Truthy. Si es False no lo agregara en el html resultante-->
    {% if name == 'Daniel' %}
        <h1>¡Soy yo!</h1>
    {% elif name == 'Felipe'%}
        <h1>Hola amigo de la infancia</h1>
    {% else %}
        <h1>No te conozco</h1>
    {% endif %}
        
```
- **for tag**

```
<h2>Tecnologias que domino</h2>
    <ul>
        <!--Permite añadir el html que pasemos entre los tag por cada iteracion del iterable o la lista stack-->
        {% for tecnologia in stack%}
            <li>{{tecnologia}}</li>
        {% empty %}
            <li>No hay tecnologias por mostrar</li>
        {% endfor %}
    </ul>
    {% comment %}  
    Este tag permite agregar un comentario que solo se mostrara en el servidor, no sera agregado al
    html que se enviara al usuario.

    Aqui vemos como podemoms cargar la lista directamente en el html, y se vera en el mismo formato
    que se muestra en el string cuando se imprime su representacion en cadena en la terminal
    {% endcomment %}
    <h2>{{stack}}</h2>

    <!--Acceder a los elementos de una lista con indexacion en html-->
    <ul>
        <li>{{stack.0}}</li>
        <li>{{stack.1}}</li>
        <li>{{stack.2}}</li>
        <li>{{stack.3}}</li>
        <li>{{stack.4}}</li>
    </ul>
```

- **url tag:** Permite añadir una url en el template html de forma dinamica solo especificando el name de esta y django se encargara de obtener y agregar el path completo al template html.

```
{% for tecnologia in stack%}
    <!--django remplaza el tag de url por el path completo que le proporcionemosy se agregara en cualquier
    parte de la web que lo agreguemos-->
    <li><a href="{% url 'stack' tool=tecnologia.id %}">{{tecnologia.name}}</a></li>
{% empty %} 
    <li>No hay tecnologias por mostrar</li>
{% endfor %}
```

