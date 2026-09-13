from logica import (buscar_por_nombre, filtrar_por_categoria,
                    listar_categorias, calcular_resumen)


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
    print("0. Finalizar")
