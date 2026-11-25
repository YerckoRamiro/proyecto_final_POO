# Mi módulo: Pagos y Clientes – Sabor Valluno (variante D)

Autora: Anahi Mishele Barrios Choquetarqui. Rama: `feature/pagos-clientes`.
Archivos: `modelo/pagos.py`, `modelo/clientes.py` y mi sección de `pruebas.py`. Bitácora: `docs/registro_ia_barrios.md`.

## Reglas del CLAUDE.md que aplican a mi módulo
1. Sin `isinstance`, `type()`, lambdas, comprensiones de lista, `@dataclass` ni `Enum`.
2. Atributos protegidos (`_nombre`) con `@property` y setters que validan y lanzan `ValueError` con mensaje claro.
3. `Pago` hereda de `ABC` y tiene `@abstractmethod`. `Pago()` lanza `TypeError`. Cada hija implementa todos los métodos abstractos.
4. Las hijas llaman a `super().__init__(...)` y no repiten atributos del padre.
5. Dinero en Bs, con `round(x, 2)`.
6. Comentarios cortos en español, sin código muerto.
7. Valores de la variante en minúscula en el diagrama (`recargo`) son atributos de clase protegidos (`_recargo = 0.03`) con property de solo lectura. Las constantes en MAYÚSCULAS (`LARGO_CODIGO`) son públicas.
8. Visibilidad del diagrama: `+` público, `#` protegido, `-` privado (solo `Cliente.correo` y `Cliente.password`).

## modelo/pagos.py
| Clase | Atributos | Métodos |
| --- | --- | --- |
| `Pago` (A) | `_nombre`, `_monto_base`, `_fecha_hora` (se llenan en `procesar_pago`) | abstractos: `calcular_monto()`, `procesar_pago(total)`, `acepta_delivery()` |
| `PagoEfectivo(Pago)` | `_monto_recibido` (número mayor a 0), `_cambio` | `calcular_cambio()` = recibido − monto_base. `calcular_monto()` = monto_base. `procesar_pago` exige recibido ≥ total. Acepta delivery |
| `PagoQr(Pago)` | `_cod_trans` (exactamente `LARGO_CODIGO` = 10 dígitos) | `calcular_monto()` = monto_base. Acepta delivery |
| `PagoTarjeta(Pago)` | `_recargo` = 0.03 (property `recargo`) | `calcular_comision()` = monto_base × recargo. `calcular_monto()` = monto_base + comisión. NO acepta delivery |

`procesar_pago(total)` valida que el total sea mayor a 0, guarda `monto_base` y `fecha_hora` y devuelve el texto del comprobante.

## modelo/clientes.py
`Cliente(nombre, celular, correo, password, direccion)`:
- `_nombre` (no vacío), `_celular` (8 dígitos, empieza en 6 o 7), `_direccion` (no vacía): protegidos con property.
- `__correo`: privado, con property.
- `__password`: privado, SIN property de lectura. Se compara con `verificar_password(texto)`, que devuelve `True` o `False`.

## Decisiones tomadas (no están en el CLAUDE.md, se pueden cambiar)
- Correo, contraseña y dirección no pueden estar vacíos (misma regla que el nombre).
- El monto recibido en efectivo debe ser un número mayor a 0.

## Preguntas tipo defensa para practicar
**Pago y herencia**
1. ¿Por qué `Pago` es abstracta? ¿Qué pasa si hago `Pago("x")`?
2. ¿Qué pasa si `PagoQr` no implementa `acepta_delivery`?
3. ¿Por qué las hijas llaman a `super().__init__("Efectivo")`?

**PagoEfectivo y PagoQr**
4. ¿Qué pasa si el cliente paga Bs 40 un pedido de Bs 41? ¿Y si paga justo Bs 41? (error; cambio 0)
5. ¿Qué pasa si el código QR tiene 9 dígitos o letras? (`ValueError`)
6. Cambio en vivo: ¿cómo hago que el QR acepte códigos de 12 dígitos? (cambiar `LARGO_CODIGO`)

**PagoTarjeta**
7. Total Bs 100: ¿cuánto es la comisión y cuánto paga el cliente? (3,00 y 103,00)
8. ¿Por qué `recargo` es de solo lectura? ¿Cómo cambio el 3 % a 5 %? (cambiar `_recargo`)
9. ¿Por qué la tarjeta no se acepta en delivery y quién lo usa? (`PedidoDelivery.puede_pagar_con` llama a `pago.acepta_delivery()`)

**Cliente**
10. ¿Qué pasa con el celular "51234567"? ¿Y con "7123"? (`ValueError` en los dos)
11. ¿Por qué `password` no tiene property de lectura? ¿Cómo se comprueba una contraseña?
12. ¿Qué diferencia hay entre `_nombre` y `__correo`? (protegido vs privado con name mangling)