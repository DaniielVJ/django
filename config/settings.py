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
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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

