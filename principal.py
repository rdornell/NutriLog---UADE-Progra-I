
from modelo import catalogo, consumos
from interfaz import (mostrar_menu, mostrar_alimentos, mostrar_consumos, mostrar_resumen,
                      opcion_buscar_alimento, opcion_filtrar_categoria,
                      opcion_cargar_alimento, opcion_registrar_consumo)


def main():
    opcion = ""
    while opcion != "0":
        mostrar_menu()
        opcion = input("Opcion: ").strip()
        if opcion == "1":
            mostrar_alimentos(catalogo)
        elif opcion == "2":
            opcion_buscar_alimento(catalogo)
        elif opcion == "3":
            opcion_filtrar_categoria(catalogo)
        elif opcion == "4":
            opcion_cargar_alimento(catalogo)
        elif opcion == "5":
            opcion_registrar_consumo(catalogo, consumos)
        elif opcion == "6":
            mostrar_consumos(consumos)
        elif opcion == "7":
            mostrar_resumen(consumos)
        elif opcion == "0":
            print("Hasta luego.")
        else:
            print("Opcion invalida. Elija un numero del menu.")


main()
