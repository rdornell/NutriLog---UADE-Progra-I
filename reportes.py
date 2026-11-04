from logica import calcular_resumen
from modelo import NUTRIENTES, mostrar_fecha


def calcular_referencia(perfil, tabla):
    for fila in tabla:
        if fila["sexo"] == perfil["sexo"] and fila["actividad"] == perfil["actividad"]:
            if perfil["sexo"] == "f":
                ajuste = -161
            else:
                ajuste = 5
            basal = (10 * perfil["peso"] + 6.25 * perfil["altura"]
                     - 5 * perfil["edad"] + ajuste)
            calorias = basal * fila["factor"]
            return {"calorias": round(calorias, 2),
                    "proteinas": round(calorias * 0.20 / 4, 2),
                    "carbohidratos": round(calorias * 0.50 / 4, 2),
                    "grasas": round(calorias * 0.30 / 9, 2)}
    return None


def comparar(consumo, referencia):
    # margen del 10% para considerar adecuado el consumo
    porcentaje = round(consumo / referencia * 100, 2)
    if porcentaje < 90:
        estado = "deficit"
    elif porcentaje > 110:
        estado = "exceso"
    else:
        estado = "adecuado"
    return porcentaje, estado


def reporte_del_rango(consumos, desde, hasta, referencia):
    por_dia = {}
    for consumo in consumos:
        fecha = consumo["fecha"]
        if fecha >= desde and fecha <= hasta:
            if fecha not in por_dia:
                por_dia[fecha] = []
            por_dia[fecha].append(consumo)
    if not por_dia:
        return []

    resumenes = []
    for registros in por_dia.values():
        resumenes.append(calcular_resumen(registros))
    # matriz: una fila por nutriente y una columna por cada dato del reporte
    filas = []
    for nutriente in NUTRIENTES:
        valores = []
        for resumen in resumenes:
            valores.append(resumen[nutriente])
        dentro = "-"
        fuera = "-"
        if referencia:
            dentro = 0
            for valor in valores:
                porcentaje, estado = comparar(valor, referencia[nutriente])
                if estado == "adecuado":
                    dentro += 1
            fuera = len(valores) - dentro
        filas.append([nutriente, round(sum(valores) / len(valores), 2),
                      min(valores), max(valores), dentro, fuera])
    return filas


ENCABEZADOS = ("Nutriente", "Promedio", "Minimo", "Maximo", "Dias dentro", "Dias fuera")


def texto_reporte(desde, hasta, filas):
    titulo = "Reporte del " + mostrar_fecha(desde) + " al " + mostrar_fecha(hasta)
    lineas = [titulo, " | ".join(ENCABEZADOS)]
    for fila in filas:
        columnas = []
        for valor in fila:
            columnas.append(str(valor))
        lineas.append(" | ".join(columnas))
    return "\n".join(lineas)


def exportar_reporte(desde, hasta, filas):
    nombre = "reporte_" + desde + "_" + hasta
    with open(nombre + ".txt", "w", encoding="utf-8") as archivo:
        archivo.write(texto_reporte(desde, hasta, filas) + "\n")
    with open(nombre + ".csv", "w", encoding="utf-8") as archivo:
        archivo.write("Desde,Hasta," + ",".join(ENCABEZADOS) + "\n")
        for fila in filas:
            columnas = [mostrar_fecha(desde), mostrar_fecha(hasta)]
            for valor in fila:
                columnas.append(str(valor))
            archivo.write(",".join(columnas) + "\n")
