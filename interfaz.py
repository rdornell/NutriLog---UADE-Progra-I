from modelo import fecha_valida, convertir_fecha
from logica import (buscar_alimento, buscar_por_nombre, filtrar_por_categoria,
                    listar_categorias, agregar_alimento, registrar_consumo,
                    calcular_resumen, es_numero)


def mostrar_alimentos(lista_alimentos):
    if len(lista_alimentos) == 0:
        print("No hay alimentos para mostrar.")
        return
    print()
    print("Valores cada 100 gramos:")
    for alimento in lista_alimentos:
        print("- " + alimento["nombre"] + " (" + alimento["categoria"] + ")")
        print("    Calorias: " + str(alimento["calorias"]) +
              " | Proteinas: " + str(alimento["proteinas"]) + " g" +
              " | Carbohidratos: " + str(alimento["carbohidratos"]) + " g" +
              " | Grasas: " + str(alimento["grasas"]) + " g")


def mostrar_consumos(lista_consumos):
    if len(lista_consumos) == 0:
        print("Todavia no hay consumos registrados en la jornada.")
        return
    print()
    print("Consumos de la jornada:")
    for consumo in lista_consumos:
        print("- " + consumo["nombre"] + ": " + str(consumo["gramos"]) + " g")
        print("    Calorias: " + str(consumo["calorias"]) +
              " | Proteinas: " + str(consumo["proteinas"]) + " g" +
              " | Carbohidratos: " + str(consumo["carbohidratos"]) + " g" +
              " | Grasas: " + str(consumo["grasas"]) + " g")


def mostrar_resumen(lista_consumos):
    if len(lista_consumos) == 0:
        print("Todavia no hay consumos registrados en la jornada.")
        return
    resumen = calcular_resumen(lista_consumos)
    print()
    print("Resumen de la jornada (" + str(len(lista_consumos)) + " consumos):")
    print("    Calorias: " + str(resumen["calorias"]))
    print("    Proteinas: " + str(resumen["proteinas"]) + " g")
    print("    Carbohidratos: " + str(resumen["carbohidratos"]) + " g")
    print("    Grasas: " + str(resumen["grasas"]) + " g")


def opcion_buscar_alimento(lista_alimentos):
    texto = input("Nombre o parte del nombre: ").strip()
    while texto == "":
        print("El nombre no puede estar vacio.")
        texto = input("Nombre o parte del nombre: ").strip()

    encontrados = buscar_por_nombre(lista_alimentos, texto)
    if len(encontrados) == 0:
        print("No se encontraron alimentos con ese nombre.")
    else:
        mostrar_alimentos(encontrados)


def opcion_filtrar_categoria(lista_alimentos):
    categorias = listar_categorias(lista_alimentos)
    print("Categorias disponibles: " + ", ".join(categorias))

    categoria = input("Categoria: ").strip()
    while categoria == "":
        print("La categoria no puede estar vacia.")
        categoria = input("Categoria: ").strip()

    encontrados = filtrar_por_categoria(lista_alimentos, categoria)
    if len(encontrados) == 0:
        print("No hay alimentos en esa categoria.")
    else:
        mostrar_alimentos(encontrados)


def opcion_cargar_alimento(lista_alimentos):
    nombre = input("Nombre del alimento: ").strip()
    while nombre == "":
        print("El nombre no puede estar vacio.")
        nombre = input("Nombre del alimento: ").strip()

    if buscar_alimento(lista_alimentos, nombre) is not None:
        print("Ya existe un alimento con ese nombre. No se cargo.")
        return

    categoria = input("Categoria: ").strip()
    while categoria == "":
        print("La categoria no puede estar vacia.")
        categoria = input("Categoria: ").strip()

    calorias = -1
    while calorias < 0:
        entrada = input("Calorias cada 100 g: ")
        if es_numero(entrada):
            calorias = float(entrada)
        else:
            print("Tiene que ser un numero positivo, por ejemplo 12.5")

    proteinas = -1
    while proteinas < 0:
        entrada = input("Proteinas cada 100 g: ")
        if es_numero(entrada):
            proteinas = float(entrada)
        else:
            print("Tiene que ser un numero positivo, por ejemplo 12.5")

    carbohidratos = -1
    while carbohidratos < 0:
        entrada = input("Carbohidratos cada 100 g: ")
        if es_numero(entrada):
            carbohidratos = float(entrada)
        else:
            print("Tiene que ser un numero positivo, por ejemplo 12.5")

    grasas = -1
    while grasas < 0:
        entrada = input("Grasas cada 100 g: ")
        if es_numero(entrada):
            grasas = float(entrada)
        else:
            print("Tiene que ser un numero positivo, por ejemplo 12.5")

    agregar_alimento(lista_alimentos, nombre, categoria,
                     calorias, proteinas, carbohidratos, grasas)
    print("El alimento " + nombre + " se cargo al catalogo.")


def elegir_alimento(lista_alimentos, texto):
    # busca por nombre completo y si no, acepta una sola coincidencia parcial
    alimento = buscar_alimento(lista_alimentos, texto)
    if alimento is None:
        encontrados = buscar_por_nombre(lista_alimentos, texto)
        if len(encontrados) == 0:
            print("No se encontro ese alimento en el catalogo.")
            return
        if len(encontrados) > 1:
            print("Hay varias coincidencias, escriba el nombre completo:")
            mostrar_alimentos(encontrados)
            return
        alimento = encontrados[0]

    return alimento


def pedir_numero(mensaje, minimo, maximo, anterior):
    valor = None
    while valor is None:
        entrada = input(mensaje).strip()
        if entrada == "" and anterior is not None:
            valor = anterior
        elif es_numero(entrada) and float(entrada) >= minimo and float(entrada) <= maximo:
            valor = float(entrada)
        else:
            print(f"Ingrese un numero entre {minimo} y {maximo}.")
    return valor


def pedir_gramos(anterior):
    return pedir_numero("Cantidad en gramos: ", 0.001, 1000000, anterior)


def opcion_registrar_consumo(lista_alimentos, lista_consumos, jornada):
    texto = input("Nombre del alimento consumido (Enter para volver): ").strip()
    if not texto:
        return
    alimento = elegir_alimento(lista_alimentos, texto)
    if alimento is None:
        return
    gramos = pedir_gramos(None)
    fecha = pedir_fecha("Ingrese la fecha del consumo (DD/MM/AAAA, Enter para la jornada): ", jornada, True)
    consumo = registrar_consumo(lista_consumos, alimento, gramos, fecha)
    print("Se registro el consumo de " + str(gramos) + " g de " + alimento["nombre"] + ".")
    print("Aporte: " + str(consumo["calorias"]) + " calorias.")


def pedir_fecha(mensaje, jornada, usar_jornada):
    fecha = None
    while fecha is None:
        texto = input(mensaje).strip()
        convertida = convertir_fecha(texto)
        if jornada is not None and usar_jornada and texto == "":
            fecha = jornada
        elif not fecha_valida(convertida):
            print("Ingrese una fecha valida con formato DD/MM/AAAA.")
        elif jornada is not None and convertida > jornada:
            print("La fecha no puede ser posterior a la jornada ingresada.")
        else:
            fecha = convertida
    return fecha


def mostrar_menu():
    print()
    print("===== NutriLog =====")
    print("1. Ver catalogo de alimentos")
    print("2. Buscar alimento por nombre")
    print("3. Filtrar alimentos por categoria")
    print("4. Cargar alimento nuevo")
    print("5. Registrar consumo")
    print("6. Ver consumos de la jornada")
    print("7. Ver resumen de la jornada")
    print("8. Consultar un dia del historial")
    print("0. Finalizar")
