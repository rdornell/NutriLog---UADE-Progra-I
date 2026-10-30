from archivos import cargar_lista
from logica import consumos_del_dia
from modelo import catalogo, mostrar_fecha, alimento_valido, consumo_valido
from interfaz import (mostrar_menu, mostrar_alimentos, mostrar_consumos, mostrar_resumen,
                      opcion_buscar_alimento, opcion_filtrar_categoria,
                      opcion_cargar_alimento, opcion_registrar_consumo, pedir_fecha)


def main():
    alimentos = cargar_lista("catalogo.json", catalogo, alimento_valido)
    consumos = cargar_lista("consumos.json", [], consumo_valido)
    jornada = pedir_fecha("Ingrese la fecha de la jornada (DD/MM/AAAA): ", None, False)
    opcion = ""
    while opcion != "0":
        mostrar_menu()
        opcion = input("Opcion: ").strip()
        if opcion == "1":
            mostrar_alimentos(alimentos)
        elif opcion == "2":
            opcion_buscar_alimento(alimentos)
        elif opcion == "3":
            opcion_filtrar_categoria(alimentos)
        elif opcion == "4":
            opcion_cargar_alimento(alimentos)
        elif opcion == "5":
            opcion_registrar_consumo(alimentos, consumos, jornada)
        elif opcion == "6":
            mostrar_consumos(consumos_del_dia(consumos, jornada))
        elif opcion == "7":
            mostrar_resumen(consumos_del_dia(consumos, jornada))
        elif opcion == "8":
            fecha = pedir_fecha("Ingrese la fecha a consultar (DD/MM/AAAA): ", None, False)
            registros = consumos_del_dia(consumos, fecha)
            print("Fecha: " + mostrar_fecha(fecha))
            mostrar_consumos(registros)
            if registros:
                mostrar_resumen(registros)
        elif opcion == "0":
            print("Hasta luego.")
        else:
            print("Opcion invalida. Elija un numero del menu.")


main()
