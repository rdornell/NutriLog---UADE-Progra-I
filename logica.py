import re
from modelo import NUTRIENTES


def buscar_alimento(lista_alimentos, nombre):
    for alimento in lista_alimentos:
        if alimento["nombre"].lower() == nombre.lower():
            return alimento
    return None


def buscar_por_nombre(lista_alimentos, texto):
    texto = texto.lower()
    return list(filter(lambda alimento: texto in alimento["nombre"].lower(), lista_alimentos))


def filtrar_por_categoria(lista_alimentos, categoria):
    encontrados = []
    for alimento in lista_alimentos:
        if alimento["categoria"].lower() == categoria.lower():
            encontrados.append(alimento)
    return encontrados


def listar_categorias(lista_alimentos):
    categorias = []
    vistas = set()
    for alimento in lista_alimentos:
        categoria = alimento["categoria"]
        if categoria.lower() not in vistas:
            vistas.add(categoria.lower())
            categorias.append(categoria)
    return categorias


def agregar_alimento(lista_alimentos, nombre, categoria, calorias, proteinas, carbohidratos, grasas):
    nuevo_alimento = {
        "nombre": nombre,
        "categoria": categoria,
        "calorias": calorias,
        "proteinas": proteinas,
        "carbohidratos": carbohidratos,
        "grasas": grasas,
    }
    lista_alimentos.append(nuevo_alimento)


def calcular_aporte(alimento, gramos):
    # regla de tres: los valores del catalogo son cada 100 g
    proporcion = gramos / 100
    aporte = {}
    for nutriente in NUTRIENTES:
        aporte[nutriente] = round(alimento[nutriente] * proporcion, 2)
    return aporte


def registrar_consumo(lista_consumos, alimento, gramos, fecha):
    consumo = {"nombre": alimento["nombre"], "fecha": fecha, "gramos": gramos, "base": {}}
    for nutriente in NUTRIENTES:
        consumo["base"][nutriente] = alimento[nutriente]
    consumo.update(calcular_aporte(alimento, gramos))
    lista_consumos.append(consumo)
    return consumo


def calcular_resumen(lista_consumos):
    resumen = {}
    for nutriente in NUTRIENTES:
        total = 0
        for consumo in lista_consumos:
            total = total + consumo[nutriente]
        resumen[nutriente] = round(total, 2)
    return resumen


def es_numero(texto):
    # entero con una parte decimal opcional: 150 o 12.5
    return re.match("^[0-9]+(\\.[0-9]+)?$", texto) is not None


def consumos_del_dia(lista_consumos, fecha):
    encontrados = []
    for consumo in lista_consumos:
        if consumo["fecha"] == fecha:
            encontrados.append(consumo)
    return encontrados


def editar_consumo(consumo, gramos, fecha):
    nuevo = consumo.copy()
    if gramos != consumo["gramos"]:
        if "base" in consumo:
            nuevo.update(calcular_aporte(consumo["base"], gramos))
        else:
            proporcion = gramos / consumo["gramos"]
            for clave in NUTRIENTES:
                nuevo[clave] = round(consumo[clave] * proporcion, 2)
    nuevo["gramos"] = gramos
    nuevo["fecha"] = fecha
    return nuevo
