from archivos import guardar_lista
from modelo import ACTIVIDADES, NUTRIENTES, RANGOS_PERFIL, fecha_valida, convertir_fecha
from reportes import calcular_referencia, comparar
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


def mostrar_resumen(lista_consumos, referencia):
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
    if referencia:
        print("Comparacion con los valores diarios de referencia:")
        for nutriente in NUTRIENTES:
            porcentaje, estado = comparar(resumen[nutriente], referencia[nutriente])
            print(f"    {nutriente}: {porcentaje} % de {referencia[nutriente]} ({estado})")


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

    valores = []
    for nutriente in NUTRIENTES:
        valores.append(pedir_numero(nutriente.capitalize() + " cada 100 g: ", 0, 1000000, None))
    agregar_alimento(lista_alimentos, nombre, categoria,
                     valores[0], valores[1], valores[2], valores[3])
    if not guardar_lista("catalogo.json", lista_alimentos):
        lista_alimentos.pop()
        return
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
    if not guardar_lista("consumos.json", lista_consumos):
        lista_consumos.pop()
        return
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


def pedir_opcion(mensaje, opciones):
    valor = input(mensaje).strip().lower()
    while valor not in opciones:
        print("Opciones disponibles: " + ", ".join(opciones))
        valor = input(mensaje).strip().lower()
    return valor


def pedir_dato_perfil(campo, mensaje):
    minimo, maximo = RANGOS_PERFIL[campo]
    valor = pedir_numero(mensaje, minimo, maximo, None)
    if campo != "edad":
        return valor
    while valor != int(valor):
        print("La edad tiene que ser un numero entero.")
        valor = pedir_numero(mensaje, minimo, maximo, None)
    return int(valor)


def opcion_perfil(perfiles, tabla):
    if perfiles:
        perfil = perfiles[0]
        print(f"{perfil['nombre']} | {perfil['edad']} anios | sexo: {perfil['sexo']} | "
              f"{perfil['peso']} kg | {perfil['altura']} cm | actividad {perfil['actividad']}")
        referencia = calcular_referencia(perfil, tabla)
        if referencia:
            print("Valores diarios de referencia:", referencia)
        if pedir_opcion("Editar perfil? (s/n): ", ("s", "n")) == "n":
            return

    nombre = input("Nombre (Enter para volver): ").strip()
    if not nombre:
        return
    perfil = {"nombre": nombre, "edad": pedir_dato_perfil("edad", "Edad: "),
              "sexo": pedir_opcion("Sexo biologico (f/m): ", ("f", "m")),
              "peso": pedir_dato_perfil("peso", "Peso en kg: "),
              "altura": pedir_dato_perfil("altura", "Altura en cm: "),
              "actividad": pedir_opcion("Actividad (baja/media/alta): ", ACTIVIDADES)}
    if guardar_lista("perfil.json", [perfil]):
        perfiles.clear()
        perfiles.append(perfil)
        print("Perfil guardado.")
        referencia = calcular_referencia(perfil, tabla)
        if referencia:
            print("Valores diarios de referencia:", referencia)
        else:
            print("No se pudo calcular una referencia con los datos y la tabla actuales.")


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
    print("9. Ver o editar el perfil")
    print("0. Finalizar")
