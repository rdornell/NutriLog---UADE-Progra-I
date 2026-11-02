import re


NUTRIENTES = ("calorias", "proteinas", "carbohidratos", "grasas")
ACTIVIDADES = ("baja", "media", "alta")
RANGOS_PERFIL = {"edad": (18, 120), "peso": (30, 350), "altura": (100, 250)}

# Catalogo de alimentos de prueba, valores cada 100 gramos
catalogo = [
    {"nombre": "Arroz blanco", "categoria": "Cereales",
     "calorias": 130.0, "proteinas": 2.7, "carbohidratos": 28.0, "grasas": 0.3},
    {"nombre": "Pechuga de pollo", "categoria": "Carnes",
     "calorias": 165.0, "proteinas": 31.0, "carbohidratos": 0.0, "grasas": 3.6},
    {"nombre": "Huevo", "categoria": "Carnes",
     "calorias": 155.0, "proteinas": 13.0, "carbohidratos": 1.1, "grasas": 11.0},
    {"nombre": "Banana", "categoria": "Frutas",
     "calorias": 89.0, "proteinas": 1.1, "carbohidratos": 22.8, "grasas": 0.3},
    {"nombre": "Manzana", "categoria": "Frutas",
     "calorias": 52.0, "proteinas": 0.3, "carbohidratos": 13.8, "grasas": 0.2},
    {"nombre": "Leche entera", "categoria": "Lacteos",
     "calorias": 61.0, "proteinas": 3.2, "carbohidratos": 4.8, "grasas": 3.3},
    {"nombre": "Lentejas", "categoria": "Legumbres",
     "calorias": 116.0, "proteinas": 9.0, "carbohidratos": 20.1, "grasas": 0.4},
    {"nombre": "Pan integral", "categoria": "Cereales",
     "calorias": 247.0, "proteinas": 13.0, "carbohidratos": 41.0, "grasas": 3.4},
]

def tiene_texto(dato, clave):
    return type(dato.get(clave)) == str and dato[clave].strip() != ""


def tiene_numero(dato, clave):
    valor = dato.get(clave)
    return type(valor) in (int, float) and valor >= 0


def fecha_valida(fecha):
    if re.match("^[0-9]{4}-[0-9]{2}-[0-9]{2}$", fecha) is None:
        return False
    anio, mes, dia = fecha.split("-")
    anio = int(anio)
    mes = int(mes)
    dia = int(dia)
    if anio == 0 or mes < 1 or mes > 12:
        return False
    dias = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return dia >= 1 and dia <= dias[mes - 1]

def convertir_fecha(texto):
    """Pasa una fecha escrita como DD/MM/AAAA al formato interno AAAA-MM-DD."""
    if re.match("^[0-9]{2}/[0-9]{2}/[0-9]{4}$", texto) is None:
        return ""
    dia, mes, anio = texto.split("/")
    return anio + "-" + mes + "-" + dia


def mostrar_fecha(fecha):
    """Pasa una fecha guardada como AAAA-MM-DD a DD/MM/AAAA para mostrarla."""
    anio, mes, dia = fecha.split("-")
    return dia + "/" + mes + "/" + anio


def nutrientes_validos(dato):
    for clave in NUTRIENTES:
        if not tiene_numero(dato, clave):
            return False
    return True


def alimento_valido(dato):
    return (type(dato) == dict and tiene_texto(dato, "nombre")
            and tiene_texto(dato, "categoria")
            and nutrientes_validos(dato))


def consumo_valido(dato):
    if type(dato) != dict or not tiene_texto(dato, "fecha"):
        return False
    if not fecha_valida(dato["fecha"]):
        return False
    base = dato.get("base")
    if "base" in dato and (type(base) != dict
                           or not nutrientes_validos(base)):
        return False
    return (tiene_texto(dato, "nombre")
            and tiene_numero(dato, "gramos") and dato["gramos"] > 0
            and nutrientes_validos(dato))


def perfil_valido(perfil):
    if type(perfil) != dict or not tiene_texto(perfil, "nombre"):
        return False
    if perfil.get("sexo") not in ("f", "m") or perfil.get("actividad") not in ACTIVIDADES:
        return False
    if type(perfil.get("edad")) != int:
        return False
    for campo in RANGOS_PERFIL:
        minimo, maximo = RANGOS_PERFIL[campo]
        if not tiene_numero(perfil, campo):
            return False
        if perfil[campo] < minimo or perfil[campo] > maximo:
            return False
    return True


def fila_referencia_valida(fila):
    return (type(fila) == dict and fila.get("sexo") in ("f", "m")
            and fila.get("actividad") in ACTIVIDADES and tiene_numero(fila, "factor")
            and fila["factor"] >= 1 and fila["factor"] <= 3)
