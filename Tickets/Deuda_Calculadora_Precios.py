# calculadora_precios.py
# Archivo encontrado en servidor de FoodExpress
# No tocar? parece que funciona...

def calc(precio, desc, prop, env, usuario):
    # calcula el total
    a = precio
    if desc > 0:
        a = precio - (precio * desc / 100)
    else:
        a = precio
    
    b = a + prop
    
    if env == "delivery":
        if a < 10000:
            b = b + 3000
        else:
            b = b + 1000
    else:
        b = b
    
    c = b
    
    # descuento especial para usuarios VIP (campo 5 en usuario)
    if len(usuario) > 4:
        if usuario[4] == "VIP":
            c = c * 0.9
    
    # redondeo
    import math
    d = math.ceil(c)
    
    # impuesto?
    if d > 50000:
        d = d * 1.19
    
    # formato
    total = "$" + str(int(d))
    return total

def aplicar_cupon(total, cupon):
    # aplica cupon de descuento
    if cupon == "BIENVENIDA10":
        total = total * 0.9
    elif cupon == "NAVIDAD20":
        total = total * 0.8
    elif cupon == "LIBRE":
        total = 0
    else:
        total = total
    return total

def calcular_propina(subtotal, porcentaje):
    # calcula propina
    prop = subtotal * (porcentaje / 100)
    if prop > 10000:
        prop = 10000  # tope maximo propina
    return prop

# funcion principal que parece usarse desde la web
def get_total(precio_plato, descuento, propina_porcentaje, tipo_entrega, datos_usuario, codigo_cupon):
    try:
        p = float(precio_plato)
        d = float(descuento)
        prop = calcular_propina(p, float(propina_porcentaje))
        total_parcial = calc(p, d, prop, tipo_entrega, datos_usuario)
        total_final = aplicar_cupon(total_parcial, codigo_cupon)
        return total_final
    except:
        return "ERROR"