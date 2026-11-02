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
