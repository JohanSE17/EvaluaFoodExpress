# test_calculadora_precios.py — pruebas unitarias básicas
# Estas pruebas sirven como base para el CI; aseguran que el comportamiento
# central de la calculadora se mantenga estable ante cambios.

from Tickets.Fix_Calculadora_Precios import get_total, aplicar_cupon, calcular_propina


def test_cupon_navidad20():
    # El cupón NAVIDAD20 debe aplicar un 20% de descuento sobre el precio base.
    resultado = get_total(20000, 0, 0, "local", {}, "NAVIDAD20")
    assert resultado == "$16.000", f"Esperado $16.000, obtenido {resultado}"


def test_descuento_vip():
    # Usuarios VIP tienen un 10% de descuento adicional (aplicado antes de impuestos).
    usuario_vip = {"tipo": "VIP", "nombre": "Ana"}
    resultado = get_total(30000, 0, 0, "local", usuario_vip, "")
    assert resultado == "$27.000", f"Esperado $27.000, obtenido {resultado}"


def test_entrada_invalida():
    # Si pasan un precio no numérico, el sistema debe responder con un error legible.
    resultado = get_total("abc", 0, 0, "delivery", {}, "")
    assert "ERROR" in resultado


def test_propina_sobre_subtotal():
    # La propina se calcula sobre el subtotal ya descontado, no sobre el precio original.
    propina = calcular_propina(10000, 10)
    assert propina == 1000, f"Esperado 1000, obtenido {propina}"
