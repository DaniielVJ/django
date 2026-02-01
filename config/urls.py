from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .admin_config import configurar_panel_django_admin
# include, permite incluir rutas que tengamos definidas en otro modulo distinto al principal (ROOT_URLCONF)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Se pasa como argumento la ruta al modulo que contiene las urls que queremos incluir
    path('messages/', include('quotes.urls')), # Para usar o acceder a las rutas del modulo que incluimos, se debe hacer a traves 
    # de la ruta que definimos como primer argumento en la funcion path
    path('landings/', include('landing.urls')),
    path('minilibrary/', include('minilibrary.urls'))
]


# La funcion static, permite registrar una url y una carpeta para poder servir los archivos de esta usando la url
if settings.DEBUG:
    # Enlaza la url al path de un directorio en el servidor, donde se iran a buscar los archivos que se pidan por la url, igual como lo hace /static/ en las carpetas static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

configurar_panel_django_admin()
