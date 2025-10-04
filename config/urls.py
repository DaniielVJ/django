from django.contrib import admin
from django.urls import path, include

# include, permite incluir rutas que tengamos definidas en otro modulo distinto al principal (ROOT_URLCONF)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Se pasa como argumento la ruta al modulo que contiene las urls que queremos incluir
    path('messages/', include('quotes.urls')), # Para usar o acceder a las rutas del modulo que incluimos, se debe hacer a traves 
    # de la ruta que definimos como primer argumento en la funcion path
    path('landings/', include('landing.urls'))
]
