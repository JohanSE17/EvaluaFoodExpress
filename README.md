# FoodExpress - Análisis de Deuda Técnica en Calculadora de Precios

## SOBRE EL PROBLEMA

### Archivo Python antiguo

Han encontrado un archivo Python antiguo en el servidor de FoodExpress. Nadie sabe quién lo escribió, pero parece ser el core del cálculo de precios de los pedidos.

### La Burguer Queen

El dueño del restaurante "La Burguer Queen" se queja de que los precios a veces no coinciden con lo que deberían cobrar. Ustedes deben analizar este código.

El archivo se llama `calculadora_precios.py` y actualmente está en producción: [https://catalogocuadrosesencia.my.canva.site/prepared-by](https://catalogocuadrosesencia.my.canva.site/prepared-by)

## Preguntas de análisis

### ¿Qué tipo de mantenimiento predomina? ¿Qué significa esto para el sistema?

Predominan el **Correctivo** y el **Perfectivo** (3 cada uno). Esto es una señal de alerta: significa que el sistema ya tiene bugs activos en producción que afectan el dinero de los restaurantes, y al mismo tiempo el código está tan mal escrito que es difícil arreglarlos sin introducir nuevos errores. Es un círculo vicioso típico de la deuda técnica acumulada.

**Advertencia**: Si no se atacan los Correctivos primero (P1, P2), el negocio sigue perdiendo dinero cada día. Si no se pagan los Perfectivos después (P4, P5), el sistema seguirá siendo frágil y cada nuevo cambio tomará el triple de tiempo.

### ¿Hay problemas que podrían clasificarse en más de un tipo? ¿Cuáles?

Sí, **P3** (retornar string con "$") es el caso más claro: es **Correctivo** porque ya está causando el fallo del cupón NAVIDAD20, pero también es **Perfectivo** porque mezclar formato de presentación con lógica de cálculo es un problema de diseño que afectará cualquier funcionalidad futura que use el precio.

P4 también tiene una dimensión Correctiva potencial: si ya existe un rol "SUPERVIP" en la base de datos y nadie lo detectó, estaría dando descuentos indebidos hoy.

### ¿Qué problemas son más urgentes de resolver? ¿Por qué?

En orden de urgencia:

- **I1 y I2**: afectan directamente el dinero. Los restaurantes están cobrando mal y los clientes están pagando montos incorrectos. Cada hora sin arreglar es pérdida económica real.
- **I3**: el cupón NAVIDAD20 nunca ha funcionado bien. Al ser diciembre el mes del problema, tiene impacto directo en ventas y confianza del usuario.
- **I3 y I4**: no causan daño inmediato comprobado, pero aumentan la probabilidad de nuevos bugs cada vez que alguien toque el código.

### ¿Qué partes del código refactorizarían (preventivo)?

Las acciones de refactorización preventiva prioritarias serían:

- Renombrar toda la función y sus parámetros (**I5**): `cp` → `calcular_precio_total`, `p` → `precio_base`, `t` → `subtotal`, etc. Es la refactorización con mayor retorno: reduce el tiempo de comprensión de minutos a segundos.
- Separar responsabilidades: `cp()` hace demasiado. Extraer funciones pequeñas: `aplicar_descuento()`, `calcular_envio()`, `aplicar_vip()`, `aplicar_impuesto()`. Cada una testeable por separado.
- Mover `import math` al inicio del módulo (**I6**) y agregar validación de tipos con un bloque `try/except ValueError` específico.
- Agregar pruebas unitarias para cada función extraída. Con cobertura del 70% mínimo, cualquier cambio futuro se valida automáticamente antes de llegar a producción.

**Éxito**: Pagar esta deuda técnica hoy evita que los próximos 12 incidentes de diciembre del año siguiente sean igual de difíciles de diagnosticar.

## Problema identificado

La función `get_total()` llama a `calc()`, que devuelve un string con formato "$12000". Luego ese string se pasa a `aplicar_cupon()`, que intenta multiplicarlo por 0.8; operación imposible sobre texto. El resultado es que ningún cupón funciona. Adicionalmente, el impuesto del 19% se aplica después del redondeo, generando centavos perdidos.

En palabras simples: es como si la calculadora mostrara el precio en pantalla y luego alguien intentara hacer más cuentas sobre la pantalla en lugar de sobre el número real.

## Solución técnica

- **Separar el formato del cálculo**: `calc()` debe devolver un número (`float`), no un string con "$". El formato "$XXXX" se aplica solo al final, una sola vez, justo antes de mostrarle el resultado al usuario.
- **Corregir el orden de operaciones**: el flujo correcto es: precio → descuento → envío → VIP → propina → impuesto → redondeo → formato.
- **Aplicar cupón sobre número**: `aplicar_cupon()` recibe y devuelve siempre un `float`, nunca un string.

## Estructura del proyecto

- `Tickets/`: Contiene los archivos relacionados con la calculadora de precios.
  - `Fix_Calculadora_Precios.py`: Versión corregida de la calculadora.
  - `test_calculadora.py`: Pruebas unitarias con pytest.
- `.github/workflows/`: Configuración de CI/CD con GitHub Actions.
  - `python-tests.yml`: Workflow para linting, tests y coverage en múltiples versiones de Python.

## Cómo ejecutar las pruebas

```bash
pytest -q
```

## CI/CD

El proyecto incluye un workflow de GitHub Actions que ejecuta:
- Linting con Ruff
- Tests unitarios con pytest
- Reporte de coverage
- En versiones de Python 3.10, 3.11 y 3.12
