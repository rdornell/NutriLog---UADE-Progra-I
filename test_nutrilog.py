from logica import buscar_alimento, calcular_aporte, consumos_del_dia, editar_consumo, registrar_comida, registrar_consumo, sumar_gramos
from modelo import catalogo, consumo_valido
from reportes import comparar, reporte_del_rango


def test_aporte_proporcional():
    banana = buscar_alimento(catalogo, "Banana")
    assert calcular_aporte(banana, 150) == {
        "calorias": 133.5, "proteinas": 1.65, "carbohidratos": 34.2, "grasas": 0.45
    }


def test_cambiar_fecha_y_cantidad():
    banana = buscar_alimento(catalogo, "Banana")
    registros = []
    registro = registrar_consumo(registros, banana, 150, "2026-11-09")
    registros[0] = editar_consumo(registro, 300, "2026-11-10")
    assert consumos_del_dia(registros, "2026-11-09") == []
    assert consumos_del_dia(registros, "2026-11-10")[0]["calorias"] == 267.0


def test_comida_compuesta():
    banana = buscar_alimento(catalogo, "Banana")
    partes = []
    for gramos in (25, 50, 100):
        registrar_consumo(partes, banana, gramos, "2026-11-09")
    comida = {"nombre": "Merienda", "componentes": partes}
    registros = []
    registro = registrar_comida(registros, comida, "2026-11-10")
    assert consumo_valido(registro)
    assert len(registros) == 1
    assert registro["gramos"] == 175
    assert registro["calorias"] == 155.75


def test_reporte_por_dia():
    banana = buscar_alimento(catalogo, "Banana")
    registros = []
    registrar_consumo(registros, banana, 150, "2026-11-09")
    registrar_consumo(registros, banana, 300, "2026-11-10")
    filas = reporte_del_rango(registros, "2026-11-09", "2026-11-11", None)
    assert filas[0] == ["calorias", 200.25, 133.5, 267.0, "-", "-"]


def test_comparar():
    assert comparar(50, 100) == (50.0, "deficit")
    assert comparar(110, 100) == (110.0, "adecuado")
    assert comparar(111, 100) == (111.0, "exceso")


def test_sumar_gramos_recursivo():
    partes = [{"gramos": 100}, {"gramos": 50}, {"gramos": 25}]
    assert sumar_gramos(partes) == 175
    assert sumar_gramos([]) == 0
