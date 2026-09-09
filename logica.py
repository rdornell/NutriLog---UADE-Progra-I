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
