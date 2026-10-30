import json
def cargar_lista(nombre, inicial, validar):
    try:
        with open(nombre, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        if type(datos) != list:
            raise ValueError("Formato incorrecto")
        for dato in datos:
            if not validar(dato):
                raise ValueError("Formato incorrecto")
        return datos
    except FileNotFoundError:
        return inicial.copy()
    except Exception:
        print("No se pudo leer " + nombre + ". Se usaran datos iniciales.")
        return inicial.copy()


def guardar_lista(nombre, datos):
    try:
        with open(nombre, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
        return True
    except Exception:
        print("No se pudo guardar " + nombre + ".")
        return False
