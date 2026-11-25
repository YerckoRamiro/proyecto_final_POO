# Guía de defensa – Sabor Valluno (variante D)

Defensa de 10 minutos sin IA: (1) explicar el diagrama v2 y los cambios (2 min), (2) explicar un fragmento de código (3 min),
(3) cambio en vivo (4 min), (4) pregunta de traza (1 min). Los cambios de abajo se probaron en una copia del proyecto.

## 1. Cambios en vivo de VALORES (cambiar una línea)

Regla de oro: el docente pregunta "¿dónde está esa regla?". Se responde con el nombre de la constante y el archivo.
Los números de línea pueden moverse: busca el nombre con Ctrl+F.

| Pedido del docente | Archivo y constante | Cambio | ¿Qué prueba falla después? |
| --- | --- | --- | --- |
| Descuento del combo 15 % → 20 % | `productos.py`, `_descuento` | `_descuento = 0.20` | Combo de 3 productos (productos) |
| Descuento desde 2 productos en vez de 3 | `productos.py`, `_min_producto` | `_min_producto = 2` | Caso de referencia 41 (productos) |
| La jarra cuesta 2 vasos | `productos.py`, `VASOS_POR_JARRA` | `= 2` | Jarra (productos) |
| Comisión de tarjeta 3 % → 4 % | `pagos.py`, `_recargo` | `_recargo = 0.04` | ninguna (falta la prueba) |
| **Quitar la comisión de tarjeta** | `pagos.py`, `_recargo` | `_recargo = 0` | ninguna (falta la prueba) |
| Envase Bs 2 → Bs 3 por plato | `pedidos.py`, `_costo_envase` | `= 3` | Reporte de para llevar (integración) |
| **Quitar el envase** | `pedidos.py`, `_costo_envase` | `= 0` | Reporte de para llevar (integración) |
| Descuento local 5 % → 10 % | `pedidos.py`, `_desc_grupo` | `= 0.10` | ninguna (falta la prueba) |
| Descuento local desde 4 platos | `pedidos.py`, `_platos_des` | `= 4` | ninguna (falta la prueba) |
| Pedido mínimo delivery Bs 60 → 50 | `pedidos.py`, `_pedido_minimo` | `= 50` | ninguna (falta la prueba) |
| Mesas del 1 al 20 | `pedidos.py`, `_mesa_max` | `= 20` | Mesa 16 (integración) |
| Cantidad máxima 20 → 10 | `pedidos.py`, `CANTIDAD_MAX` | `= 10` | ninguna (falta la prueba) |
| Cambiar el envío de Cercado a Bs 10 | `pedidos.py`, `ZONAS` | `"Cercado": 10` | ninguna (falta la prueba) |
| Zona nueva Tiquipaya a Bs 18 | `pedidos.py`, `ZONAS` | agregar `"Tiquipaya": 18` | Zona inválida (integración): la prueba usaba Tiquipaya como zona inexistente |
| **Quitar el cobro de envío** | `pedidos.py`, `PedidoDelivery.calcular_cargos` | `return 0` | Total del delivery = 97 (integración) |
| El delivery acepta tarjeta | `pagos.py`, `PagoTarjeta.acepta_delivery` | `return True` | ninguna (falta la prueba) |
| El QR tiene 12 dígitos | `pagos.py`, `LARGO_CODIGO` | `= 12` | ninguna (falta la prueba) |
| El chicharrón también el sábado | datos en `main.py` / pruebas | `Plato("Chicharron", 45, ["sabado", "domingo"])` | — |

Qué se explica después del cambio: "ejecuté `python pruebas.py` y falla la prueba X porque su valor esperado era el anterior".
Si NO falla ninguna prueba, es una señal de que falta cubrir esa regla: hay que agregar la prueba.

**Por qué es una línea:** cada regla de la variante es un atributo de clase protegido con property (`_descuento` + `descuento`).
Nadie repite el número en otro lugar. Por eso el cambio no toca a `Combo`, `Pedido` ni `Restaurante`.

## 2. Cambios en vivo con CÓDIGO NUEVO (polimorfismo real)

### Postre (el más probable)
"Postre: precio base más Bs 3 si lleva crema; no cuenta como plato para los envases."
Se agrega al final de `productos.py` y NO se toca `Combo`, `Pedido` ni `Restaurante`:

```python
class Postre(Producto):
    # precio base mas Bs 3 si lleva crema; no cuenta como plato (no paga envase)
    _extra_crema = 3

    def __init__(self, nombre, precio, con_crema=False):
        super().__init__(nombre, precio)
        self._con_crema = con_crema

    def calcular_precio(self):
        if self._con_crema:
            return round(self.precio + self._extra_crema, 2)
        return round(self.precio, 2)

    def esta_disponible(self, dia):
        return True

    def contar_platos(self):
        return 0
```

Comprobado: un flan con crema (10 + 3) vale 13; el combo (silpancho 35 + flan 13 + mocochinchi 6) × 0,85 = 45,90 y tiene 1 plato;
en un pedido para llevar de 2 combos + 1 flan los envases son Bs 4 (el postre no cuenta). Aparece en el menú de cualquier día.

Si el docente pregunta "¿por qué no tocaste Pedido?": porque `Pedido` solo llama a `calcular_precio()`, `esta_disponible()` y
`contar_platos()`, y cada producto sabe responderlas. Eso es polimorfismo.

### Método de pago nuevo (por ejemplo, transferencia)
Se agrega una clase hija de `Pago` en `pagos.py` con sus 3 métodos abstractos (`calcular_monto`, `procesar_pago`, `acepta_delivery`).
No se toca `Restaurante`: `cobrar_pedido` ya llama a `puede_pagar_con(pago)` y `procesar_pago(...)`.
Comprobado: la transferencia se cobra en para llevar y es aceptada en delivery (si `acepta_delivery` devuelve `True`).

### Otro tipo de pedido
Una hija de `Pedido` con `calcular_cargos`, `calcular_descuento`, `obtener_tipo` y `validar_para_preparar`.
`Restaurante.reporte_ventas_dia()` lo agrupa solo, porque usa `obtener_tipo()`.

### Otras pruebas de cambio que pueden pedir
- "Agrega un día de venta al plato" → se pasa en la lista `dias_disponibles`, sin tocar el código.
- "Que el delivery sea gratis desde Bs 150" → en `calcular_cargos` de `PedidoDelivery`: `if self.calcular_subtotal() >= 150: return 0`.
  Esta regla es de las variantes A, B, C, E y F; la D no la tiene, así que se explica por qué la D no la tiene.
- "Que el cliente tenga puntos" → atributo `_puntos` con property en `Cliente`.

## 3. Preguntas por pilar

### Abstracción
1. ¿Qué clases son abstractas y por qué? (`Producto`, `Pedido`, `Pago`: son conceptos generales, no existe un "producto" suelto.)
2. ¿Qué pasa si hago `Producto("x", 10)`? (`TypeError`: faltan los métodos abstractos.)
3. ¿Qué pasa si una hija no implementa un método abstracto? (No se puede instanciar la hija.)
4. Si quito `ABC` pero dejo `@abstractmethod`, ¿se sigue protegiendo? (No: sin `ABC` el decorador no hace nada.)
5. ¿Por qué `contiene_a` NO es abstracto y `calcular_precio` sí? (`contiene_a` tiene una respuesta válida por defecto: `self is producto`; el precio no.)
6. ¿Cuáles son los métodos abstractos de `Pedido` y quién los implementa? (`calcular_cargos`, `calcular_descuento`, `obtener_tipo`, `validar_para_preparar`; las 3 hijas.)
7. ¿Para qué sirve que `Pago` tenga `acepta_delivery()` abstracto? (Cada pago decide; el pedido no pregunta qué tipo es.)

### Herencia
1. ¿Cuántas subclases hay? (9: Plato, Bebida, Combo, PedidoLocal, PedidoLlevar, PedidoDelivery, PagoEfectivo, PagoQr, PagoTarjeta.)
2. ¿Qué hace `super().__init__(...)` y qué pasaría sin él? (Inicializa los atributos del padre; faltaría `_nombre` o `_precio`.)
3. ¿Por qué `Bebida` no tiene un atributo `_precio_vaso`? (Está en el padre como `precio`; `precio_vaso` es una property que lo devuelve; repetirlo rompe la herencia.)
4. ¿Qué atributos heredan los tres pedidos? (`_numero`, `_cliente`, `_estado`, `_items`, `_fecha_hora`, `_dia`, `_pago`.)
5. ¿Por qué `Combo` es un `Producto`? (Así un combo puede ir dentro de otro combo y dentro de un pedido igual que un plato.)
6. ¿Por qué se valida `len(productos) < 2` antes de `super().__init__`? (Para mostrar el error real y no un error de precio.)

### Polimorfismo
1. Da un ejemplo de método sobrescrito. (`calcular_precio()` en Plato, Bebida y Combo.)
2. ¿Cómo calcula `Combo` su precio si dentro hay otro combo? (Llama a `calcular_precio()` de cada hijo; el hijo combo repite el proceso.)
3. ¿Dónde está el `if` por tipo? (En ninguna parte: no hay `isinstance`, `type()` ni `if/elif` por tipo.)
4. `Restaurante.crear_pedido_local` evita mesas duplicadas, ¿cómo sin `isinstance`? (Llama a `ocupa_mesa(mesa)`; `Pedido` devuelve `False` por defecto y solo `PedidoLocal` lo sobrescribe.)
5. ¿Cómo sabe el delivery que la tarjeta no vale? (`puede_pagar_con(pago)` llama a `pago.acepta_delivery()`.)
6. ¿Cómo agrupa el reporte por tipo? (Con `obtener_tipo()`, que devuelve "Local", "Para llevar" o "Delivery".)
7. ¿Cómo se cuentan los envases dentro de un combo? (`contar_platos()`: plato = 1, bebida = 0, combo = suma de sus hijos × cantidad.)
8. `calcular_vaso()` tiene `if self._tipo == "jarra"`: ¿es un if por tipo? (No: es un valor del atributo `tipo` dentro de una misma clase, no el tipo de la clase.)

### Encapsulación
1. ¿Por qué `_nombre` lleva guion bajo y se lee con `@property`? (Protegido: nadie lo cambia sin pasar por el setter que valida.)
2. ¿Qué diferencia hay entre `_x` y `__x`? (`_x` es protegido por convención; `__x` es privado con name mangling: `Cliente.__password`.)
3. ¿Por qué `password` no tiene property de lectura? (Es un dato privado; solo se puede comprobar con `verificar_password(texto)`.)
4. ¿Por qué `items` devuelve `list(self._items)`? (Una copia: modificar la copia no cambia el pedido.)
5. ¿Por qué `cantidad` en `PedidoProducto` no tiene setter? (Si lo tuviera, se podría cambiar la cantidad con el pedido en EN_PREPARACION; para sumar se reemplaza el ítem.)
6. ¿Dónde se valida el precio > 0? (Solo en el setter de `Producto`.)
7. `self.precio = precio` en el constructor, ¿por qué no `self._precio = precio`? (Para pasar por el setter y validar al crear.)
8. ¿Qué atributos del diagrama son privados `-`? (`correo` y `password` de Cliente.)

## 4. Preguntas de traza (calculadas con la variante D)

| Pregunta | Cuenta | Resultado |
| --- | --- | --- |
| Combo clásico: silpancho 35 + mocochinchi 6 | 41 (2 unidades, sin descuento) | **Bs 41,00** |
| Combo clásico + sopa de maní 18 + jarra de mocochinchi (18) | (41 + 18 + 18) × 0,85, son 3 unidades | **Bs 65,45** |
| 2 silpanchos + 1 mocochinchi en un combo | (70 + 6) × 0,85 | **Bs 64,60** |
| Delivery a Quillacollo con 2 combos clásicos | 82 + 15 de envío | **Bs 97,00** |
| Local con 6 silpanchos | 210 − 5 % (10,50) | **Bs 199,50** |
| Para llevar: 3 combos clásicos + 2 vasos | subtotal 135 + envases 3 platos × 2 = 6 | **Bs 141,00** |
| Delivery a Cercado con 1 silpancho | 35 < 60 | **Error: pedido mínimo Bs 60** |
| Pagar 141 con efectivo de 200 | 200 − 141 | **Cambio Bs 59,00** |
| Pagar 199,50 con tarjeta | 199,50 × 1,03 | **Bs 205,48** (ver aviso) |

**Aviso del redondeo:** 199,50 × 3 % = 5,985. A mano se redondea a 5,99, pero Python da 5,98 (total 205,48) porque guarda el decimal en binario.
Si el docente lo calcula a mano, explica esa diferencia; el equipo debe decidir cuál es el valor que defiende.

## 5. Preguntas "¿qué pasa si...?"
- ¿... agrego un combo dentro de sí mismo? → `ValueError` (`contiene_a` detecta el ciclo directo e indirecto).
- ¿... agrego un chicharrón a un pedido el martes? → `ValueError`: no está disponible ese día.
- ¿... un combo tiene el chicharrón y lo pido el martes? → tampoco: un combo está disponible solo si todos sus productos lo están.
- ¿... cambio el precio del silpancho después de armar el combo? → el combo se actualiza solo, porque calcula en vivo; `combo.precio` NO se actualiza (es el precio inicial).
- ¿... cancelo un pedido EN_PREPARACION? → `ValueError`: solo se cancela desde REGISTRADO.
- ¿... agrego un producto con el pedido LISTO? → `ValueError`: solo en REGISTRADO.
- ¿... cobro un pedido REGISTRADO, cancelado o ya pagado? → `ValueError` en los tres casos.
- ¿... pago en efectivo con menos del total? → `ValueError` y el pedido NO queda pagado (primero se procesa el pago, después se marca).
- ¿... registro dos clientes con el mismo celular? → `ValueError` (supuesto 5).
- ¿... un pedido para llevar sin cliente? → `ValueError` (supuesto 8).
- ¿... la mesa 5 ya tiene un pedido abierto? → `ValueError`; si se cancela o entrega, se libera.

## 6. Preguntas sobre el diagrama, la variante y el proceso
- ¿Qué cambió del diagrama v1 al v2? (tipos y visibilidad; `max_producto` → `min_producto`; se quita la herencia Cliente → Pago; se agrega `Restaurante` y los métodos de la lógica.)
- Muestra en el diagrama dónde se relaciona `Combo` con `Producto`. (Herencia `Producto ◁── Combo` y composición `Combo ◆── ComboProducto ──▶ Producto`.)
- ¿Qué es composición y qué es agregación en tu diagrama? (Composición: `Pedido ◆ PedidoProducto`, la parte no existe sola; agregación: `Restaurante ◇ Producto`.)
- ¿De dónde sale el 15 %? (Variante D: 15 % solo con 3 o más productos; está en `Combo._descuento` y `_min_producto`.)
- ¿Por qué la variante D no tiene envío gratis? (La tabla de la consigna dice "Sin envío gratis".)
- ¿Cuáles de tus reglas son supuestos no consultados? (Los 8 del acta; cada uno está marcado con `# SUPUESTO:`.)
- ¿Por qué no se implementó la regla 9 (retraso en delivery)? (El docente indicó que no se incluye; está en el acta.)
- ¿Cuánto usaste IA y en qué? (Está en la bitácora; hay que responder con sinceridad y poder explicar el código.)
- ¿Por qué se trabajó en ramas y con Pull Request? (Cada una toca solo sus archivos y otra persona revisa antes de unir.)

## 7. Cómo practicar
1. Con cronómetro, 4 minutos por cambio. Quien hace de docente elige uno de la tabla de la sección 1 y otro de la sección 2.
2. Después de cada cambio: `python pruebas.py` y explicar qué prueba falló y por qué.
3. Volver el código al estado original con `git checkout -- <archivo>` (en una rama de práctica, nunca en `main`).
4. Cada integrante explica su módulo a las otras en 10 minutos, sin mirar el código.
