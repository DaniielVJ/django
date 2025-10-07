from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.urls import reverse

# Si el dia que el usuario envia coincide con alguna clave del diccionario
# devolveremos la palabra asociada a esa clave o dia
days_of_week={
    'monday': 'Pienso, Luego existo',
    'tuesday': 'La vida es un sueño',
    'wednesday': 'El conocimiento es poder',
    'thursday': 'Sé el cambio que quieras ver',
    'friday': 'Solo se que no se nada',
    'saturday': 'Vive como si fuera el ultimo dia',
    'sunday': 'Da un poquito mas todos los dias'
}


def home(request):
    days=list(days_of_week.keys())
    return render(request, 'quotes/home.html', {'days': days})

# Generamos HTML desde string y lo enviamos al cliente
def index(request):
    list_items = ""
    days=list(days_of_week.keys())
    for day in days:
        # permite obtener el path completo a traves del name
        redirect_path=reverse('day-quote', args=[day])
        list_items+=f"<li><a href='{redirect_path}'>{day.capitalize()}</a></li>"
    
    response_html = "<ul>" + list_items + "</ul>"
    return HttpResponse(response_html)

    # Con comprehensionList
    elemento_li_dia=[f'<li><a href={redirect_path}>{day.capitalize()}</a></li>' for day in days]
    

# si el day se manda como integer se acciona esta vista
def days_week_with_number(request, day):
    # Forma del profesor
    days=list(days_of_week.keys())
    if day > len(days): # si pasa numero mayor a la cantidad de dias
        return HttpResponseNotFound('<h1>El dia no existe</h1>')        
    redirect_day=days[day-1] # con 0 en day accede a sunday 0-1=-1
    
    # reverse, regresa la url completa del path que especifiquemos su nombre, desde la url del proyecto
    # en args se pasa como argumento el valor que le daremos si el path es dinamico.
    redirect_path = reverse('day-quote', args=[redirect_day])
    return HttpResponseRedirect(redirect_path)
    
    # Mi forma de reenviarlos a la ruta del dia correspondiente segun el numero de dia que pasen
    days=dict(enumerate(days_of_week.keys(), 1))
    print(days)
    # Respondemos con una redireccion a otra ruta
    return HttpResponseRedirect(f'/quotes/{days.get(day, 'desconocido')}')


# Si el dia se manda como texto acciona esta vista
def days_week(request, day):
    if day not in days_of_week:
        # Si no se encuentra el dia podemos lanzar una excepcion 404 que incluye django que permitira
        # mandar un 404 al usuario, ahora esto nos puede lanzar error si se usa con el debug=True en el modo de
        # desarrollo pero no asustarse pq en produccion lanzara el template para 404
        # Este de forma automatica django buscara en los templates un archivo 404.html asegurarnos de llamar el archivo html
        # como el codigo de estado
        raise Http404() # No la capturamos nosotros, porque queremos que django maneje esa excepcion, no nosotros
        # return render(request, '404.html', status=404) # plantilla personalizada
    return render(request, 'quotes/day.html', {'day':day, 'message': days_of_week[day]})
   

    # Version del profe
    try:
        quote_text=days_of_week[day]
        return HttpResponse(quote_text)
    except KeyError:
        return HttpResponseNotFound("No hay frase para ese dia")

