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
e igualmente dentro del html para usar los valores que enviamos de python debemos escribir en el lenguaje de plantillas, para indicar a django que estamos escribiendo en lenguaje de plantillas en vez de html usamos llaves {} y dentro de esta escribimos en el lenguaje de plantillas. ahora los valores de variable se cargan con llaves igualmente dentro de las llaves del lenguaje de plantillas. EJ:
```    
<h2>Hola {{name}}</h2>
```
