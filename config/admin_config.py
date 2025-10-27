from django.contrib import admin

def configurar_panel_django_admin():
    # Modifica el titulo del header del djando admin
    admin.site.site_header = "Administrador MiniLibrary"
    # Este es el titulo que se muestra en la pestaña al abrir el admin
    admin.site.site_title = "MiniLibrary panel"
    # Este es el Titulo que esta abajo del header y arriba de los modelos de cada app
    admin.site.index_title = "Bienvenido al panel de minilibrary"

