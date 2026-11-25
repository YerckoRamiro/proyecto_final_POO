# CLAUDE.md – Proyecto Integrador POO: Sistema de pedidos "Sabor Valluno" (variante D)

## Contexto
Proyecto universitario de Programación Orientada a Objetos. Python 3, aplicación de consola, solo biblioteca estándar.
Equipo: Yercko Ramiro Nina Gomez, Maria Liz Quispe Mamani, Anahi Mishele Barrios Choquetarqui.
La defensa es oral y SIN IA: el docente elige cualquier fragmento del código, pide cambios en vivo y hace preguntas tipo
"¿qué pasa si...?". Por eso el código debe ser simple, coherente con el diagrama de clases y explicable por cada integrante.
Tu trabajo (Claude Code) es ayudarnos a construirlo Y a entenderlo, no solo a que funcione.
La interfaz es de consola, simple y clara. No hacemos interfaz gráfica ni nada "bonito": importa la lógica.

## Reglas del código (no negociables)
1. Solo biblioteca estándar. Consola con input() y print().
2. Solo construcciones vistas en clase: clases, herencia, `super()`, `@property` con `@nombre.setter`, `ABC` con
   `@abstractmethod`, listas, diccionarios, `for`, `if`, excepciones (`raise ValueError("mensaje")` y `try/except`), f-strings,
   `datetime` para fecha y hora.
   PROHIBIDO sin permiso del equipo: `@dataclass`, `Protocol`, `match`, `TypeVar`, `Enum`, decoradores propios, lambdas,
   comprensiones de lista (usa `for`), anotaciones de tipo, `isinstance`, `type()`.
3. Nombres en español sin tildes ni ñ. Clases en PascalCase; métodos, atributos y variables en snake_case. Idénticos al diagrama
   (`Diagramas/diagrama_v2.md`): todo lo que está en el diagrama está en el código con el mismo nombre y la misma visibilidad.
4. Encapsulación: atributos protegidos con guion bajo (`_nombre`), acceso por `@property`, setters con validación que lanzan
   `ValueError` con mensaje claro. Nadie modifica la lista de ítems desde fuera: la propiedad devuelve una copia (`list(self._items)`).
   Visibilidad en el diagrama: `+` público (métodos, properties, constantes en MAYÚSCULAS), `#` protegido (`_x` con property),
   `-` privado (`__x`, solo `Cliente.correo` y `Cliente.password`). Los valores de la variante que están en el diagrama en
   minúscula (`descuento`, `mesa_min`, `recargo`...) son atributos de clase protegidos (`_descuento = 0.15`) con property de solo lectura.
5. Polimorfismo real: PROHIBIDO `isinstance`, `type()` o `if/elif` por tipo en el modelo. Las diferencias entre tipos se
   resuelven con métodos sobrescritos.
6. Abstracción: `Producto`, `Pedido` y `Pago` heredan de `ABC` y tienen `@abstractmethod`. Instanciarlas debe lanzar
   `TypeError`. Cada subclase concreta implementa TODOS los métodos abstractos.
7. Herencia: las subclases llaman a `super().__init__(...)` y NO repiten atributos del padre. Mínimo 9 subclases (hay exactamente 9).
8. Dinero en Bs, redondeado con `round(x, 2)`.
9. Estilo: comentarios cortos en español, como los escribiría un estudiante. Sin docstrings largos, sin código muerto,
   sin `try/except` que nunca se use, sin funciones "por si acaso".
10. NUNCA inventes una regla en silencio. Si algo no está en este archivo ni en `docs/acta_consultas.md`, pregúntame. Si el equipo
    decide asumirlo, déjalo en una constante con nombre claro y el comentario `# SUPUESTO:` para poder cambiarlo en segundos.
11. Si el código que ya escribimos entra en conflicto con este archivo, NO lo borres ni lo reescribas en silencio: muéstrame la
    diferencia y propón el cambio mínimo.
12. El código es la fuente de verdad del diagrama. Todo lo que está en el diagrama v2 existe en el código con el mismo nombre,
    y viceversa.

## Variante D (reemplaza los valores base)
| Regla | Valor en variante D |
| --- | --- |
| Descuento del combo | 15 %, solo si el combo tiene 3 o más productos; con 2 productos no hay descuento |
| Envase para llevar | Bs 2 por plato (cuentan los platos dentro de combos; las bebidas no cuentan) |
| Envío gratis | No existe (nunca es gratis) |
| Pedido mínimo en delivery | Bs 60 (sobre el subtotal, sin envío) |
| Regla adicional | Pedido local con 6 platos o más: 5 % de descuento sobre el subtotal |

## Reglas base que siguen vigentes
- Menú: platos (silpancho, pique macho, chicharrón, sopa de maní), bebidas (refrescos naturales y gaseosas) y combos.
- Bebida: precio por vaso; la jarra cuesta 3 veces el precio del vaso.
- Combo: 2 o más productos (platos, bebidas u otros combos). Precio = suma de sus productos con el descuento de la variante.
  Un combo no puede contenerse a sí mismo, ni directa ni indirectamente.
- Disponibilidad: hay platos que se venden solo ciertos días (chicharrón: domingos). Un combo está disponible solo si todos sus productos lo están.
- Local: sin cargos, mesa del 1 al 15, una mesa no puede tener dos pedidos abiertos.
- Delivery: envío por zona (Cercado 8, Quillacollo 15, Sacaba 15, Vinto 20). Solo acepta efectivo o QR.
- Estados: REGISTRADO → EN_PREPARACION → LISTO → ENTREGADO. CANCELADO solo desde REGISTRADO. Solo se agregan o quitan
  productos en REGISTRADO. Un cambio inválido lanza excepción.
- Pagos: efectivo (monto recibido ≥ total, calcula el cambio), QR (código de transacción de exactamente 10 dígitos),
  tarjeta (comisión de 3 % a cargo del cliente).
- Validaciones: precio > 0; cantidad por producto en el pedido de 1 a 20; teléfono de 8 dígitos que empieza en 6 o 7.
- Regla 9 (retraso en delivery y compensación): NO se implementa. El docente indicó que no se incluye en el proyecto.
  No agregues hora de entrega, plazo de retraso ni compensación.

## Decisiones confirmadas
- Un pedido se puede cobrar en LISTO y también en ENTREGADO (no si está cancelado ni si ya fue pagado).
- Cada integrante entrega su propia bitácora de IA: `docs/registro_ia_<apellido>.md` (tres archivos, sin archivo común).

## Decisiones del equipo (24/11/2026)
- Los nombres salen del diagrama aprobado (`Diagramas/Diagrama UML poo_final.png`). El diagrama v2 (`Diagramas/diagrama_v2.md`)
  se genera desde el código y lista los cambios respecto al v1 (visibilidad, `max_producto` → `min_producto`, se quita la herencia
  `Cliente → Pago` y las líneas `ComboProducto — Pedido` y `PagoQr — Cliente`, se agrega `Restaurante`).
- Precio del Combo, opción 1: el Combo pasa a `super().__init__` la suma inicial de sus productos (así `Producto` valida precio > 0
  en un solo lugar), pero `calcular_precio()` recalcula en vivo desde sus productos y no usa `_precio`.

## Supuestos del equipo (NO consultados al docente; lectura literal de la consigna)
Cada uno va en una constante o método con el comentario `# SUPUESTO:`, y el README y el acta los declaran.
1. Combo con 2 productos: sin descuento. El "3 o más" (y el mínimo de 2) cuenta las unidades directas del combo sumando la
   cantidad de cada `ComboProducto` con `contar_productos()`: 2 silpanchos + 1 mocochinchi = 3 → 15 %. Un combo interno cuenta como 1 por unidad.
2. El chicharrón sigue vendiéndose solo los domingos (regla base; la variante D no la reemplaza).
3. El 5 % del pedido local se calcula sobre el subtotal y cuenta los platos dentro de combos (usa `contar_platos()`).
4. El pedido mínimo de Bs 60 del delivery se mide sobre el subtotal, sin el envío.
5. El celular identifica al cliente: `registrar_cliente` rechaza un celular repetido.
6. `reporte_ventas_dia()` y `top_productos()` cuentan solo pedidos pagados del día.
7. El total del reporte suma lo cobrado (`pedido.pago.calcular_monto()`), incluida la comisión de tarjeta.
8. Para llevar y delivery necesitan un cliente (`crear_pedido_para_llevar` y `crear_pedido_delivery` rechazan `None`); el local puede no tenerlo.

## Modelo de clases (nombres exactos)
Estructura: `modelo/productos.py`, `modelo/pedidos.py`, `modelo/pagos.py`, `modelo/clientes.py`, `restaurante.py`, `main.py`, `pruebas.py`.
Hay 16 clases (las 15 del diagrama aprobado + `Restaurante`). Las marcadas (A) son abstractas.
Elementos propios de la variante D (están en el diagrama): en `Combo`, `descuento` y `min_producto`; en `PedidoLocal`,
`platos_des`, `desc_grupo` y `calcular_descuento()`; en `PedidoLlevar`, `costo_envase`; en `PedidoDelivery`, `pedido_minimo`.
Todos son atributos de clase protegidos con property de solo lectura (`_descuento = 0.15` + `@property descuento`).

### modelo/productos.py
Constante de módulo `DIAS_SEMANA`: "lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo" (sin tildes, en el orden de `weekday()`).

| Clase | Atributos (protegidos, con property) | Métodos |
| --- | --- | --- |
| `Producto` (A) | `_nombre`, `_precio` (> 0, se valida SOLO aquí) | abstractos: `calcular_precio()`, `esta_disponible(dia)`, `contar_platos()`. Concreto: `contiene_a(producto)` devuelve `self is producto` |
| `Plato(Producto)` | `_dias_disponibles` (lista de días; por defecto los 7) | `calcular_precio()` = precio; `esta_disponible(dia)` = el día está en `_dias_disponibles`; `contar_platos()` = 1 |
| `Bebida(Producto)` | `_tipo` ("vaso" o "jarra"), `_categoria` ("refresco natural" o "gaseosa"); constante `VASOS_POR_JARRA` = 3; property `precio_vaso` (devuelve el `precio` del padre, sin atributo propio) | `calcular_vaso()` = 1 si es vaso, 3 si es jarra; `calcular_precio()` = `precio_vaso` × `calcular_vaso()`; siempre disponible; `contar_platos()` = 0 |
| `ComboProducto` | `_producto`, `_cantidad` (≥ 1) | `calcular_precio()` = `producto.calcular_precio()` × cantidad; `contar_platos()` = `producto.contar_platos()` × cantidad |
| `Combo(Producto)` | `_productos` (lista de `ComboProducto`, mínimo 2); constante `MIN_PRODUCTOS` = 2; `_min_producto` = 3, `_descuento` = 0.15 | `agregar_producto(producto, cantidad=1)` (rechaza si `producto.contiene_a(self)`), `quitar_producto(producto)` (nunca menos de 2), `productos` (copia), `contar_productos()` = suma de las cantidades. `calcular_precio()` = suma de `calcular_precio()` de cada `ComboProducto` × (1 − descuento) si `contar_productos()` ≥ `min_producto`, sin descuento si no. `esta_disponible(dia)` = todos disponibles. `contar_platos()` = suma de sus hijos. `contiene_a(p)` = `self is p` o algún hijo lo contiene (evita ciclos) |

### modelo/pedidos.py
| Clase | Atributos | Métodos |
| --- | --- | --- |
| `PedidoProducto` | `_pedido`, `_producto`, `_cantidad` (1 a 20, constantes `CANTIDAD_MIN` y `CANTIDAD_MAX`) | `calcular_precio()` = `producto.calcular_precio()` × cantidad; `contar_platos()` = `producto.contar_platos()` × cantidad |
| `Pedido` (A) | constantes de estado (`REGISTRADO`, `EN_PREPARACION`, `LISTO`, `ENTREGADO`, `CANCELADO`), diccionario `TRANSICIONES`, contador `_contador`, `_numero`, `_cliente`, `_estado`, `_items` (lista de `PedidoProducto`), `_fecha_hora`, `_dia`, `_pago` (el `Pago` usado, `None` si no está pagado) | concretos: `agregar_producto(producto, cantidad)` (solo REGISTRADO; verifica `esta_disponible(self._dia)`; si ya existe suma cantidades), `quitar_producto(producto)`, `calcular_subtotal()`, `contar_platos()`, `calcular_total()` = subtotal − descuento + cargos, `cambiar_estado(nuevo)`, `cancelar()`, `esta_abierto()`, `ocupa_mesa(mesa)` (False por defecto), `puede_pagar_con(pago)` (True por defecto), `marcar_pagado(pago)`, `esta_pagado()`. Abstractos: `calcular_cargos()`, `calcular_descuento()`, `obtener_tipo()`, `validar_para_preparar()` |
| `PedidoLocal(Pedido)` | `_mesa` (entre `mesa_min` = 1 y `mesa_max` = 15); `_platos_des` = 6, `_desc_grupo` = 0.05 | cargos 0; descuento `desc_grupo` del subtotal si `contar_platos()` ≥ `platos_des`; `ocupa_mesa(mesa)` = misma mesa y pedido abierto. Constructor: `PedidoLocal(mesa, cliente=None, dia=None)` |
| `PedidoLlevar(Pedido)` | `_costo_envase` = 2 | cargos = `contar_platos()` × `costo_envase`; descuento 0 |
| `PedidoDelivery(Pedido)` | `_zona`, `_direccion_ent`; diccionario `ZONAS` con su costo; `_pedido_minimo` = 60 | cargos = costo de la zona (nunca gratis); descuento 0; `validar_para_preparar()` exige subtotal ≥ `pedido_minimo`; `puede_pagar_con(pago)` = `pago.acepta_delivery()` |

El día del pedido sale de la fecha actual, pero el constructor acepta un `dia` opcional para poder probar (por ejemplo "domingo").
Un pedido está "abierto" si su estado no es ENTREGADO ni CANCELADO.
`validar_para_preparar()` se ejecuta al pasar a EN_PREPARACION; además el pedido debe tener al menos un ítem.

### modelo/pagos.py
| Clase | Atributos | Métodos |
| --- | --- | --- |
| `Pago` (A) | `_nombre`, `_monto_base` (el total del pedido), `_fecha_hora` (se llenan en `procesar_pago`) | abstractos: `calcular_monto()`, `procesar_pago(total)`, `acepta_delivery()` |
| `PagoEfectivo(Pago)` | `_monto_recibido`, `_cambio` | `calcular_cambio()` = recibido − monto_base; `calcular_monto()` = monto_base; `procesar_pago` exige recibido ≥ total; acepta delivery |
| `PagoQr(Pago)` | `_cod_trans` (exactamente `LARGO_CODIGO` = 10 dígitos) | `calcular_monto()` = monto_base; acepta delivery |
| `PagoTarjeta(Pago)` | `_recargo` = 0.03 (comisión a cargo del cliente) | `calcular_comision()` = monto_base × recargo; `calcular_monto()` = monto_base + comisión; NO acepta delivery |

`procesar_pago` devuelve el texto del comprobante.

### modelo/clientes.py
`Cliente`: `_nombre`, `_celular` (8 dígitos, empieza en 6 o 7), `__correo` (privado, con property), `__password` (privado, SIN property
de lectura), `_direccion`. Método `verificar_password(texto)`. Constructor: `Cliente(nombre, celular, correo, password, direccion)`.

### restaurante.py
`Restaurante` (gestor): `_menu`, `_clientes`, `_pedidos` (listas protegidas con properties que devuelven copia).
Métodos: `registrar_producto(producto)`, `armar_combo(nombre, productos)`, `listar_menu(dia)`,
`registrar_cliente(nombre, celular, correo, password, direccion)`, `buscar_cliente(celular)`, `crear_pedido_local(mesa)`,
`crear_pedido_para_llevar(cliente)`, `crear_pedido_delivery(cliente, zona, direccion_ent)`, `buscar_pedido(numero)`,
`cobrar_pedido(numero, pago)`, `reporte_ventas_dia()` (por tipo de pedido, usando `obtener_tipo()`), `top_productos(cantidad)`.
Para evitar mesas duplicadas recorre los pedidos y llama a `ocupa_mesa(mesa)` (sin isinstance).
Se puede cobrar un pedido LISTO o ENTREGADO (confirmado), no cancelado, no pagado y que `puede_pagar_con(pago)`.
El reporte y el top 3 cuentan solo pedidos pagados del día (supuestos 5 a 8).

### main.py
Menú de consola numerado con `while`. Opciones: registrar producto, armar combo, listar menú por día, registrar cliente,
crear pedido (local, para llevar, delivery), agregar/quitar productos, ver detalle (subtotal, descuentos, cargos, total),
cambiar estado, cobrar y mostrar comprobante, reporte del día, salir. Los errores de validación se capturan con `try/except ValueError`
y se muestran en pantalla. Datos de ejemplo cargados al iniciar para poder demostrar rápido. JSON: NO se implementa salvo que el equipo lo pida.

### pruebas.py
Solo `assert`, ejecutable con `python pruebas.py`. Secciones marcadas con comentarios (`# ===== PRUEBAS DE PRODUCTOS =====`, etc.)
para que cada integrante edite solo la suya. Mínimo 8 casos; el objetivo es ~15:
- Caso de referencia recalculado con la variante D (combo silpancho 35 + mocochinchi 6 = Bs 41,00, sin descuento por tener 2 productos).
- Combo de 3 productos con 15 % y combo que contiene otro combo.
- `Producto()`, `Pedido()` y `Pago()` lanzan `TypeError`.
- Combo que se contiene a sí mismo (directa e indirectamente) lanza error.
- Envases: platos dentro de combos cuentan, bebidas no.
- Pedido local con 6 platos: 5 %; delivery sin envío gratis; delivery bajo Bs 60 rechazado.
- Estados: transición inválida lanza error; cancelar solo desde REGISTRADO; no se agrega producto fuera de REGISTRADO.
- Pagos: efectivo insuficiente, QR con código inválido, tarjeta con 3 %, tarjeta rechazada en delivery.
- Validaciones: precio ≤ 0, cantidad 0 y 21, teléfono inválido, mesa 0 y 16, mesa con dos pedidos abiertos.

## Git y trabajo en equipo
- Cada integrante usa su propio usuario de Git. Commits pequeños (una clase o una regla), mensajes en español y en imperativo
  ("Agrega validación de precio en Producto"). Nunca commits con el nombre de otra persona. Nunca `push --force`.
- Ramas: `feature/productos`, `feature/pedidos`, `feature/pagos-clientes`, `feature/integracion`. Se une a `main` por Pull Request.
- Cada Pull Request lo revisa otra persona del equipo, que deja al menos un comentario real. Antes de unir: `python pruebas.py` pasa.
- Cada quien toca solo los archivos de su rama. Si necesitas cambiar un archivo ajeno, avisa en lugar de editarlo.

## Bitácora de IA (obligatoria y honesta)
Al iniciar cada sesión pregunta quién eres (Nina, Quispe o Barrios). Registra en `docs/registro_ia_<apellido>.md` cada uso de IA
con el formato de la consigna: N.º, fecha, herramienta (Claude Code), tipo de uso, consulta textual, qué acepté, qué modifiqué y por qué,
archivo o clase, ¿lo explico sin ayuda? Tú propones el borrador; la persona completa "qué modifiqué" y "¿lo explico sin ayuda?" con
sinceridad. No inventes entradas ni ocultes usos.

## Cómo debes trabajar con nosotros
- Antes de escribir código, di en 3 líneas qué vas a hacer y en qué archivo. Trabaja de una clase a la vez.
- Después de cada clase, explícala en lenguaje simple (máximo 5 líneas) y hazme 3 preguntas tipo defensa. Espera mi respuesta.
- Si te pido algo que rompe estas reglas, avísame en lugar de hacerlo.