from pathlib import Path


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
    'django.contrib.staticfiles',
    # Indicamos el paquete donde se encuentra la aplicacion a instalar
    'quotes',
    'landing'
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
        'DIRS': [],
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


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Indicamos que ruta debe utilizar en la url el navegador o proxy para acceder a los archivos estaticos
# de nuestro proyecto django
STATIC_URL = 'static/'

# Aqui indicamos el directorio o la ruta de la carpeta donde se encuentran los estaticos y que podran
# ser accedidos a traves de la url en STATIC_URL

# Aqui se indica cual es el tipo de campo que se usara por defecto en la clave primaria
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
