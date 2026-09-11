from logica import calcular_resumen


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
