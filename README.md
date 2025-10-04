## Templates
- Los templates son html que generaremos con para mostrar o presentar los datos al usuario desde el navegador, ya que django a traves de su lenguaje de plantillas (DTL) permite darle esteroides al html y generar interfaces al usuario para que interactuee con la aplicacion, a esta podemos agregarle codigo estatico como css, js, imagenes.s

- **Funcion reverse:**  Funcion que permite que obtengamos de forma dinamica la ruta completa de un path a traves de el name que le hayamos otorgado. y si este path tiene partes donde recibe un valor dinamico y no estatico podemos establecer cual es el valor a traves de su parametro args.

- **Crear Templates:** Como buena practica para crear los templates, para cada aplicacion crearemos una carpeta templates y ahi dentro otra carpeta con el nombre de la aplicacion. Dentro de esa ubicacion vamos crear nuestros archivos html que funcionaran como plantillas de nuestra aplicacion.

- **Habilitar los snippets de html para los django templates:** CTRL+SHIFT+P>settings.json>Agregamos la siguiente configuracion:<br>
`    "emmet.includeLanguages": {
        "django-html": "html"
    },`

- **Registrar los templates:** Para poder utilizar los templates que creemos de nuestra aplicacion, debemos registrarlos en el proyecto en el  modulo settings.py especificando las rutas de las carpetas templates de nuestras aplicaciones<br>
Podemos registrar las carpetas de forma individual para cada aplicacion:<br>
`TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Aqui proporcionamos la ruta absoluta a las carpetas donde se encuentran los templates
        'DIRS': [
            BASE_DIR / "landing" / "templates"
            ],
        'APP_DIRS': True,`

