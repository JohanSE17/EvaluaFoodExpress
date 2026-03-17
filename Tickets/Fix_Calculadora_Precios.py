# calculadora_precios.py — versión corregida
# Refactorizado por: Equipo FoodExpress - Marzo 2026
# Cambios: orden de operaciones corregido, cupones arreglados,
#          nombres descriptivos, manejo de errores con logging.

import math
import logging

logging.basicConfig(level=logging.ERROR, format="%(asctime)s — %(levelname)s — %(message)s")

PROPINA_MAXIMA = 10000
COSTO_ENVIO_BAJO = 3000   # para pedidos menores a $10.000
COSTO_ENVIO_ALTO = 1000   # para pedidos mayores o iguales a $10.000
UMBRAL_ENVIO = 10000
UMBRAL_IMPUESTO = 50000
TASA_IMPUESTO = 1.19

def calcular_descuento(precio: float, descuento_porcentaje: float) -> float:
    """Aplica un porcentaje de descuento al precio base."""
    if descuento_porcentaje > 0:
        return precio - (precio * descuento_porcentaje / 100)
    return precio

def calcular_costo_envio(precio_con_descuento: float, tipo_entrega: str) -> float:
    """Retorna el costo de envío según el tipo de entrega y el subtotal."""
    if tipo_entrega == "delivery":
        if precio_con_descuento < UMBRAL_ENVIO:
            return COSTO_ENVIO_BAJO
        return COSTO_ENVIO_ALTO
    return 0

def aplicar_descuento_vip(subtotal: float, datos_usuario: dict) -> float:
    """Aplica el 10% de descuento si el usuario es VIP.
        subtotal: valor numérico antes del descuento VIP.
        datos_usuario: diccionario con al menos la clave 'tipo'.
    """
    if isinstance(datos_usuario, dict) and datos_usuario.get("tipo") == "VIP":
        return subtotal * 0.9
    return subtotal

def aplicar_impuesto(subtotal: float) -> float:
    """Aplica IVA del 19% solo si el subtotal supera los $50.000."""
    if subtotal > UMBRAL_IMPUESTO:
        return subtotal * TASA_IMPUESTO
    return subtotal

def calcular_propina(subtotal: float, porcentaje: float) -> float:
    """Calcula la propina sobre el subtotal con descuentos aplicados.
    
    El tope máximo es de $10.000 para evitar cobros excesivos.
    """
    propina = subtotal * (porcentaje / 100)
    return min(propina, PROPINA_MAXIMA)

def aplicar_cupon(total: float, cupon: str) -> float:
    """Aplica el descuento del cupón sobre un valor NUMÉRICO.
    
    recibe y retorna float, nunca string.
    """
    cupones = {
        "BIENVENIDA10": 0.9,
        "NAVIDAD20": 0.8,
        "LIBRE": 0,
    }
    factor = cupones.get(cupon)
    if factor is not None:
        return total * factor if factor > 0 else 0
    return total

def formatear_precio(valor: float) -> str:
    """Convierte un float a string con formato de moneda. Ej: '$12.500'"""
    return "$" + f"{int(math.ceil(valor)):,}".replace(",", ".")

def get_total(precio_plato, descuento, propina_porcentaje,
              tipo_entrega, datos_usuario, codigo_cupon) -> str:
    """Función principal. Calcula el total de un pedido.
    
    Orden correcto de operaciones:
    1. Precio base → 2. Descuento → 3. Envío → 4. Propina
    → 5. VIP → 6. Cupón → 7. Impuesto → 8. Redondeo → 9. Formato
    
    Returns:
        String con precio formateado "$15.200") o "ERROR" si falla.
    """
    try:
        precio_base = float(precio_plato)
        pct_descuento = float(descuento)
        pct_propina = float(propina_porcentaje)

        precio_con_descuento = calcular_descuento(precio_base, pct_descuento)
        costo_envio = calcular_costo_envio(precio_con_descuento, tipo_entrega)
        propina = calcular_propina(precio_con_descuento, pct_propina)

        subtotal = precio_con_descuento + costo_envio + propina
        subtotal = aplicar_descuento_vip(subtotal, datos_usuario)
        subtotal = aplicar_cupon(subtotal, codigo_cupon)   # ← ahora sí recibe número
        subtotal = aplicar_impuesto(subtotal)              # ← antes del redondeo

        return formatear_precio(subtotal)

    except (ValueError, TypeError) as e:
        logging.error(f"Error en get_total: {e} | args: {precio_plato}, {descuento}, {tipo_entrega}")
        return "ERROR: valor inválido en el pedido"
    except Exception as e:
        logging.error(f"Error inesperado en get_total: {e}")
        return "ERROR: contacte al equipo técnico"