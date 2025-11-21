# En este módulo definiremos los middlewares personalizados de la aplicación


# Middleware que calcula cuando tiempo tarda una view en ejecutarse
import time
import datetime
from zoneinfo import ZoneInfo
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

class TimingViewMiddleware:
    
    def __init__(self, get_response=None):
        self.get_response = get_response
    

    # Esta funcion es la logica que ejecutara el middleware, aqui ponemos todo lo que queremos hacer cuando recibimos el request
    # y cuando recibimos el response de vuelta
    def __call__(self, request, *args, **kwargs):
        ## ANTES DE LA VIEW

        start = time.time()

        # obtenemos la respuesta del request que le proporcionamos
        response = self.get_response(request)
        
        # DESPUES DE LA VIEW
        
        duration = time.time() - start
        print(f"Tiempo de respuesta: {duration:.2f} segundos")
        
        # devolvemos el response de el request que proceso la view para que la pueda procesar otro middleware o pasarcelo a django
        # para que lo envie al usuario
        return response # ¡IMPORTANTE RETORNARLO, YA QUE ESTO ES LO QUE SE ENVIA AL USUARIO!


# Middleware bloqueador de Ips
class BlockIpAddressMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response 
        # Definimos a nuestro Middleware (instancia, objeto) lista de ips permitidas  
        self.NOT_ALLOWED_IPS = ['']

    def __call__(self, request, *args, **kwds):
        # obtener ip remota que envia el request a nuestro servidor (el usuario)
        ip_remota = request.META.get('REMOTE_ADDR')
        puerto_remoto = request.META.get('REMOTE_PORT')
        # Esto imprimiria la ip de los usuarios que envian solicitudes al servidor
        print(f'ip detectada {ip_remota}:{puerto_remoto} -  {type(ip_remota)}')
        if ip_remota in self.NOT_ALLOWED_IPS:
            return HttpResponseForbidden('Eres un usuario no permitido por este sistema tu ip {} esta bloqueada'.format(ip_remota))
        return self.get_response(request)
    

class ValidationHourMiddleware:
    def __init__(self, funcion_que_pasa_django):
        self.get_response = funcion_que_pasa_django
        # hora en que se abre la empresa y se permiten transaciones, request o solicitudes al servidor
        self.hora_apertura = datetime.time(hour=8, minute=30, second=0)
        self.hora_cierre = datetime.time(hour=19, minute=11, second=0)


    def __call__(self, request, *args, **kwds):
        hora_actual = datetime.datetime.now(ZoneInfo('America/Santiago')).time()
        
        if request.path.startswith('/admin'):
            return self.get_response(request)

        if self.hora_apertura < hora_actual and self.hora_cierre > hora_actual:
            return self.get_response(request)
        return HttpResponseForbidden(f"""<h2>Los horarios de conexión son entre <span style='color:red;'>{self.hora_apertura.strftime("%H:%M")}</span> y 
                                     las  <span style='color:red;'>{self.hora_cierre.strftime("%H:%M")}</span></h2>""")


class OfficeHourOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwds):
        now = datetime.datetime.now().hour


        if now < 9 or now > 18:
            # denegamos acceso
            return HttpResponseForbidden("AUN NO ES HORA DE TRABAJAR, EL HORARIO ES DE 9AM A 6PM")
        return self.get_response(request)


EXCEPT_URLS = ['/minilibrary/login', '/admin/', '/register/']

class RequireLoginMiddleware:
    
    def __init__(self, get_response):
        self.get_response =get_response
    
    # Mi version
    def __call__(self, request, *args, **kwds):        
        if request.user.is_authenticated or any(request.path.startswith(url) for url in EXCEPT_URLS):
            return self.get_response(request)
        
        return redirect('/admin/')

        # si no esta autenticado, pasa a True y evalua lo de las url, si ninguna url iterada comienza con la que quiere el usuario False
        # y pasamos a true y redirigimos.
        # Si no esta autenticado, pasa True, asi que no hay corto circuito y evalua las url, ahora si la request su ruta comienza con una de las
        # url que especificamos any devuelve True con que una se cumpla para no redirigir el not pasa a False se lo salta y pasa el request
        # a la view.
        # Se autentica el usuario, si el usuario no esta autenticado, pero en este caso lo esta asi que devuelve True y not lo pasa  a False
        # logrando que se salte evaluar cualquier url ya que al pasar a False el primer valor todo and da False asi que corto circuito
        # saltamos el bloque que redirige y empezamos a pasar el request a cualquier view.
        if (not request.user.is_authenticated) and not any(request.path.startswith(url) for url in EXCEPT_URLS):
            print("Usuario no autenticado, redirigiendo....")
            return redirect('/admin/')

        return self.get_response(request)

        








# def middleware(get_response):
#     def codigo_ejecutado_en_llamada(request, *args, **kwargs):
#         print("CODIGO EN REQUEST")
#         response = get_response(request)
#         print("CODIGO CUANDO RESPONSE LA VISTA")
#         return response
#     return codigo_ejecutado_en_llamada


# # DJANGO LUEGO HACE
# midle = middleware(pasa_get_response)
# # LLAMADA O EJECUCION DEL MIDDLEWARE
# midle(request, otros_parametros, keywordarguments)