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
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

configurar_panel_django_admin()
