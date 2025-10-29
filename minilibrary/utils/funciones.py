from datetime import date

def formateador_fecha(fecha_string):
    # Aqui verifico que sea truthy el valor, pero si no simplemente puedo omitir este if
    # colocando este formateo dentro del if del filtro
    if fecha_string:
        fecha_fragmentada = fecha_string.split("-")
        return date(int(fecha_fragmentada[0]), int(fecha_fragmentada[1]), int(fecha_fragmentada[2]))