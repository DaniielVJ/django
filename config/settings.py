from pathlib import Path


# Se recomienda que base dir siempre almacene la ruta del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-!^4wxo6s4bc%pm(l#pu426!@@dl!73ww4gg^3lzx#ec(hwwt@_'

DEBUG = True

ALLOWED_HOSTS = []


# Aplicaciones que usara el proyecto

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Asegurarse que la aplicacion staticfiles de django este instalada, para trabajar con archivos estaticos
    'django.contrib.staticfiles',
    # Indicamos el paquete donde se encuentra la aplicacion a instalar
    'quotes',
    'landing',
    'minilibrary',
]


MIDDLEWARE = [
    # Este middleware implementa medidas de seguridad como Strict Transport Security
    'django.middleware.security.SecurityMiddleware',
    # Este middleware permite cosas como poder usar request.session en las view
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Este middleware hace tareas variadas como la de añadir slash si a una url que consulta el usuario le falta
    # como /productos pero en el sistema existe /productos/, le añade el slash final para que no haya error y coincida con la que existe 
    'django.middleware.common.CommonMiddleware',
    # Middleware encargado de verificar que si se recibe un request con POST o datos, estos vengan con un token Csrf 
    # Valido para poder pasarlo a la View
    'django.middleware.csrf.CsrfViewMiddleware',
    # Este middleware es el que permite usar un request.user, ya que es el encargado de verificar que el usuario que esta enviando request
    # esta autenticado o no
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # Este middleware permite cargar los mensajes en las respuestas HTTP 
    'django.contrib.messages.middleware.MessageMiddleware',
    # Este middleware defiende nuestra aplicación web de clickjacking, permitiendo que configuremos si nuestra aplicación web se puede
    # añadir a otra a traves de un iframe, con X_FRAME_OPTIONS = "DENY"  # o "SAMEORIGIN" en el settings.py podemos configurarla, asi
    # este añadira X-FRAME-OPTIONS en el encabezado de el response HTTP para que no pueda el template enviado ser incrustado en un iframe
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'minilibrary.middleware.TimingViewMiddleware',
    'minilibrary.middleware.BlockIpAddressMiddleware',
    # 'minilibrary.middleware.ValidationHourMiddleware',
    # 'minilibrary.middleware.OfficeHourOnlyMiddleware'
    # 'minilibrary.middleware.RequireLoginMiddleware'
    
]

# Ruta del modulo que tiene las urls que respondera el proyecto
ROOT_URLCONF = 'config.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Aqui proporcionamos la ruta absoluta a las carpetas donde se encuentran los templates
        'DIRS': [ BASE_DIR / 'templates'],
        # Habilitamos esta opcion como True, para que django cargue los templates de las aplicaciones de forma automatica
        'APP_DIRS': True, # De forma automatica buscara los templates en una carpeta templates dentro de la aplicacion
        'OPTIONS': { 
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Indicamos donde esta la interfaz que usara el servidor web para pasarle las solicitudes a la aplicacion
WSGI_APPLICATION = 'config.wsgi.application'


# Aqui configuramos que base de datos usara nuestro proyecto de django
DATABASES = {
    'default': {
        # Por defecto django utiliza sqlite para almacenar los datos del programa
        'ENGINE': 'django.db.backends.sqlite3',
        # Aqui indicamos el nombre del archivo que contiene toda la base de datos con las tablas y datos
        # de nuestras entidades en el programa
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'es-ch'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Indicamos que ruta debe utilizar en la url el navegador o proxy para acceder a los archivos estaticos
# de nuestro proyecto django
STATIC_URL = 'static/' # Es para indicar que url o location debe usar el servidor proxy para acceder a los estaticos

# Esta constante la usamos cuando tenemos carpetas con archivos estaticos fuera de las aplicaciones o que no son
# de las aplicaciones
STATICFILES_DIRS=[ # Al crearla decimos a django que cargaremos estilos de otros directorios(globales)
    BASE_DIR / 'static',
    ] 

# Esta constante indicamos la ruta a la carpeta donde se almacenaran todos los archivos estaticos del proyecto
# entero y todas las aplicaciones al momento de lanzarlo a produccion, para que un proxy server se encargue de
# servirlo.
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Aqui indicamos el directorio o la ruta de la carpeta donde se encuentran los estaticos y que podran
# ser accedidos a traves de la url en STATIC_URL

# Aqui se indica cual es el tipo de campo que se usara por defecto en la clave primaria
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Si queremos definir nuestro propio modelo usuario debemos definirlo en esta constante
# AUTH_USER_MODEL = 'miapp.models.MyUserModel'


# Define cuanto tiempo dura una session en el sistema, el valor esta en segundos
SESSION_COOKIE_AGE = 3600
# Esto define si expira o se elimina la session del usuario se cierra el navegador
SESSION_EXPIRE_AT_BROWSER_CLOSE = False # False: no expira, True: si expira
# Esta configuracion define que cada vez que envie un request, si tiene una sesion activa se renovara
# su tiempo de expiracion al que hayamos definido, es decir si es una hora si envia un request vuelve actualizarce a 1 hora mas
SESSION_SAVE_EVERY_REQUEST = True # Con esto si el usuario envia una session esta se almacenara en cada request, provocando
# que si en cada request que se envie se almacena, django al volver almacenarla renuevo su tiempo de expiracion aplazando
# al tiempo que da por defecto


# DONDE REDIRIGIRA EL LOGIN CUANDO EL USUARIO SE AUTENTIQUE Y SUS CREDENCIALES SEA VALIDAS
LOGIN_REDIRECT_URL = 'list_books'

# URL DONDE REDIRIGIRA AL USUARIO CUANDO CIERRE SESION
LOGOUT_REDIRECT_URL = 'login'

# URL DEL LOGIN, PARA CUANDO SE EJECUTEN FUNCIONES QUE REDIRIGEN AL LOGIN ESTAS SEPAN DONDE ESTA O CUAL SU URL
LOGIN_URL = 'login'