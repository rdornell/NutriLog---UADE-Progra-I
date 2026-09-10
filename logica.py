import re


def buscar_alimento(lista_alimentos, nombre):
    for alimento in lista_alimentos:
        if alimento["nombre"].lower() == nombre.lower():
            return alimento
    return None


def buscar_por_nombre(lista_alimentos, texto):
    encontrados = []
    for alimento in lista_alimentos:
        if texto.lower() in alimento["nombre"].lower():
            encontrados.append(alimento)
    return encontrados


def filtrar_por_categoria(lista_alimentos, categoria):
    encontrados = []
    for alimento in lista_alimentos:
        if alimento["categoria"].lower() == categoria.lower():
            encontrados.append(alimento)
    return encontrados


def listar_categorias(lista_alimentos):
    categorias = []
    for alimento in lista_alimentos:
        if alimento["categoria"] not in categorias:
            categorias.append(alimento["categoria"])
    return categorias


def agregar_alimento(lista_alimentos, nombre, categoria, calorias, proteinas, carbohidratos, grasas):
    if buscar_alimento(lista_alimentos, nombre) is not None:
        return False
    nuevo_alimento = {
        "nombre": nombre,
        "categoria": categoria,
        "calorias": calorias,
        "proteinas": proteinas,
        "carbohidratos": carbohidratos,
        "grasas": grasas,
    }
    lista_alimentos.append(nuevo_alimento)
    return True


def calcular_aporte(alimento, gramos):
    # regla de tres: los valores del catalogo son cada 100 g
    proporcion = gramos / 100
    aporte = {}
    aporte["calorias"] = round(alimento["calorias"] * proporcion, 2)
    aporte["proteinas"] = round(alimento["proteinas"] * proporcion, 2)
    aporte["carbohidratos"] = round(alimento["carbohidratos"] * proporcion, 2)
    aporte["grasas"] = round(alimento["grasas"] * proporcion, 2)
    return aporte


def registrar_consumo(lista_consumos, alimento, gramos):
    aporte = calcular_aporte(alimento, gramos)
    consumo = {
        "nombre": alimento["nombre"],
        "gramos": gramos,
        "calorias": aporte["calorias"],
        "proteinas": aporte["proteinas"],
        "carbohidratos": aporte["carbohidratos"],
        "grasas": aporte["grasas"],
    }
    lista_consumos.append(consumo)
    return consumo


def calcular_resumen(lista_consumos):
    total_calorias = 0
    total_proteinas = 0
    total_carbohidratos = 0
    total_grasas = 0

    for consumo in lista_consumos:
        total_calorias = total_calorias + consumo["calorias"]
        total_proteinas = total_proteinas + consumo["proteinas"]
        total_carbohidratos = total_carbohidratos + consumo["carbohidratos"]
        total_grasas = total_grasas + consumo["grasas"]

    resumen = {
        "calorias": round(total_calorias, 2),
        "proteinas": round(total_proteinas, 2),
        "carbohidratos": round(total_carbohidratos, 2),
        "grasas": round(total_grasas, 2),
    }
    return resumen


def es_numero(texto):
    # digitos, con una parte decimal opcional: 150 o 12.5
    return re.match("^[0-9]+(\\.[0-9]+)?$", texto) is not None
