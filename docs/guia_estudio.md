# Guía de estudio – Los 4 pilares de la POO en Sabor Valluno (variante D)

Para: Yercko, Maria Liz y Anahi. Cómo usarla:
1. Lee la **Parte 1** (conceptos) hasta poder explicar cada pilar con tus palabras y con un ejemplo de NUESTRO código.
2. Tápate las respuestas de las **Partes 2 a 7** y contesta en voz alta. Si dudas, vuelve a la Parte 1.
3. Practica los cambios en vivo con `docs/guia_defensa.md` (tiene la tabla probada de qué línea cambiar).

En la defensa no hay IA ni apuntes: el docente elige un fragmento, pide un cambio en vivo y pregunta "¿qué pasa si...?".

---

# PARTE 1. CONCEPTOS

## 1.1 Lo básico que se da por sabido

| Concepto | Qué es | Ejemplo nuestro |
| --- | --- | --- |
| Clase | Un molde que define atributos y métodos | `class Plato(Producto):` |
| Objeto (instancia) | Un caso concreto creado con el molde | `silpancho = Plato("Silpancho", 35)` |
| `__init__` | Constructor: se ejecuta al crear el objeto y le da sus datos iniciales | `Pedido.__init__` pone estado REGISTRADO, número, fecha y día |
| `self` | El objeto que está ejecutando el método | `self._items` es la lista de ESE pedido |
| Atributo de instancia | Dato propio de cada objeto | `self._mesa` (cada pedido local tiene su mesa) |
| Atributo de clase | Dato compartido por todos los objetos de la clase | `_descuento = 0.15` en `Combo`, `_contador` en `Pedido` |
| Método | Una función que pertenece a la clase | `calcular_total()` |
| Excepción | Un error que se lanza con `raise` y se atrapa con `try/except` | `raise ValueError("La mesa debe estar entre 1 y 15.")` |

## 1.2 ENCAPSULACIÓN

**Qué es:** proteger los datos de un objeto para que nadie los deje en un estado inválido. Se accede a ellos solo por métodos o propiedades que validan.

**Para qué sirve:** que un precio nunca sea 0, que una mesa nunca sea 16, que nadie cambie los productos de un pedido que ya está en preparación.

**Cómo se escribe en Python:**
```python
class Producto(ABC):
    def __init__(self, nombre, precio):
        self.precio = precio          # pasa por el setter: se valida al crear

    @property
    def precio(self):                 # leer: producto.precio
        return self._precio

    @precio.setter
    def precio(self, valor):          # escribir: producto.precio = 40
        if valor <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        self._precio = valor
```

**Niveles de visibilidad (y cómo están en el diagrama):**

| Símbolo UML | Nombre | En Python | Ejemplo nuestro |
| --- | --- | --- | --- |
| `+` | público | sin guion bajo (métodos y properties) | `calcular_precio()`, la property `precio` |
| `#` | protegido | un guion bajo `_x` (convención: "no lo toques desde fuera") | `_precio`, `_items`, `_estado` |
| `-` | privado | dos guiones bajos `__x` (Python le cambia el nombre: name mangling) | `Cliente.__password`, `Cliente.__correo` |

**Dónde está en nuestro proyecto:**
- Todos los atributos llevan `_` y se leen con `@property`.
- Los setters validan: precio > 0, días válidos, tipo de bebida, cantidad 1 a 20, mesa 1 a 15, zona válida, celular de 8 dígitos que empieza en 6 o 7, QR de 10 dígitos, monto recibido > 0.
- Las listas se devuelven como copia: `return list(self._items)`. Si alguien vacía la copia, el pedido no cambia.
- `PedidoProducto.cantidad` NO tiene setter: así nadie cambia la cantidad de un pedido en preparación. Para sumar, `agregar_producto` reemplaza el ítem por uno nuevo.
- `Cliente.__password` no tiene property de lectura: solo se puede comprobar con `verificar_password(texto)`.
- Las reglas de la variante son atributos de clase protegidos con property de solo lectura (`_descuento` + `descuento`), y cada una está en UN solo lugar.

**Frase para la defensa:** "Encapsular es que el objeto se proteja solo: los datos son protegidos y la única forma de cambiarlos pasa por un setter que valida y lanza ValueError."

**Trampas:**
- `_x` no es "imposible" de tocar desde fuera: es una convención. `__x` sí cambia el nombre internamente (`_Cliente__password`).
- En el constructor se escribe `self.precio = precio` (con el setter) y no `self._precio = precio`, porque si no la validación no se ejecuta al crear el objeto.

## 1.3 HERENCIA

**Qué es:** una clase hija recibe los atributos y métodos de una clase padre y puede agregar o cambiar comportamiento. Relación "ES UN": un Plato ES UN Producto.

**Para qué sirve:** no repetir código. Lo común va en el padre una sola vez; lo propio va en la hija.

**Cómo se escribe:**
```python
class Plato(Producto):                       # Plato hereda de Producto
    def __init__(self, nombre, precio, dias_disponibles=None):
        super().__init__(nombre, precio)      # el padre guarda y valida nombre y precio
        ...                                   # la hija agrega lo suyo: dias_disponibles
```

**Nuestras 3 jerarquías (9 subclases):**
- `Producto` → `Plato`, `Bebida`, `Combo`
- `Pedido` → `PedidoLocal`, `PedidoLlevar`, `PedidoDelivery`
- `Pago` → `PagoEfectivo`, `PagoQr`, `PagoTarjeta`

**Qué hereda cada una:**
- Los productos heredan `_nombre`, `_precio`, la validación de precio > 0 y `contiene_a()`.
- Los pedidos heredan número, cliente, estado, ítems, fecha, día, pago y TODOS los métodos de estados, subtotal, total y cobro.
- Los pagos heredan `_nombre`, `_monto_base` y `_fecha_hora`.

**Regla del proyecto:** las hijas llaman a `super().__init__(...)` y NO repiten atributos del padre. Ejemplo: `Bebida` no tiene `_precio_vaso`; `precio_vaso` es una property que devuelve el `precio` del padre.

**Frase para la defensa:** "La herencia pone lo común en el padre; con `super().__init__` la hija le pide al padre que inicialice su parte y ella solo agrega lo propio."

**Trampas:**
- Sin `super().__init__`, el objeto no tiene `_nombre` ni `_precio`, y falla al leer `producto.nombre`.
- `Combo` hereda de `Producto` para poder ir dentro de otro combo o de un pedido igual que un plato.

## 1.4 POLIMORFISMO

**Qué es:** el mismo mensaje (el mismo nombre de método) produce un comportamiento distinto según el objeto que lo recibe. Quien llama no necesita saber de qué clase es el objeto.

**Para qué sirve:** agregar tipos nuevos sin tocar el código que los usa, y evitar cadenas de `if` por tipo.

**Cómo se ve en nuestro código:**
```python
# Combo.calcular_precio: no pregunta si cada hijo es plato, bebida u otro combo
suma = 0
for linea in self._productos:
    suma = suma + linea.calcular_precio()     # cada hijo sabe calcular su precio
```

**Dónde está en nuestro proyecto (métodos sobrescritos):**

| Método | Quién lo sobrescribe | Qué resuelve sin `if` por tipo |
| --- | --- | --- |
| `calcular_precio()` | Plato, Bebida, Combo | Precio de cualquier producto, aunque sea un combo dentro de otro |
| `esta_disponible(dia)` | Plato, Bebida, Combo | Menú del día y productos que se pueden pedir |
| `contar_platos()` | Plato (1), Bebida (0), Combo (suma) | Envases de para llevar y 5 % del local |
| `contiene_a(producto)` | Combo | Evitar que un combo se contenga a sí mismo |
| `calcular_cargos()` | Local (0), Llevar (envases), Delivery (zona) | Total del pedido |
| `calcular_descuento()` | Local (5 % con 6 platos), Llevar y Delivery (0) | Total del pedido |
| `obtener_tipo()` | los 3 pedidos | El reporte por tipo |
| `validar_para_preparar()` | Delivery (mínimo Bs 60) | Pasar a EN_PREPARACION |
| `ocupa_mesa(mesa)` | Pedido (False por defecto), PedidoLocal | Que una mesa no tenga dos pedidos abiertos |
| `puede_pagar_con(pago)` | Pedido (True por defecto), PedidoDelivery | Delivery solo con efectivo o QR |
| `procesar_pago`, `calcular_monto`, `acepta_delivery` | los 3 pagos | Cobrar y generar el comprobante |

**Regla del proyecto:** PROHIBIDO `isinstance`, `type()` o `if/elif` por tipo en el modelo.

**Frase para la defensa:** "Polimorfismo es que `Pedido` llame a `producto.calcular_precio()` sin saber qué producto es; cada clase responde a su manera. Por eso puedo agregar un Postre sin tocar Pedido ni Combo."

**Trampas:**
- El `if self._tipo == "jarra"` de `calcular_vaso()` NO es un if por tipo de clase: compara un valor del atributo dentro de la misma clase.
- Los `if opcion == "1"` de `main.py` NO son polimorfismo falso: eligen la opción que escribió el usuario en el menú, no el tipo de un objeto.

## 1.5 ABSTRACCIÓN

**Qué es:** quedarse con lo esencial y definir un "contrato": una clase abstracta dice QUÉ deben saber hacer sus hijas, pero no CÓMO. No se puede crear un objeto de una clase abstracta.

**Para qué sirve:** obligar a que cada hija implemente los métodos necesarios. Si una hija olvida uno, Python no deja crearla.

**Cómo se escribe:**
```python
from abc import ABC, abstractmethod

class Pago(ABC):                    # hereda de ABC
    @abstractmethod
    def procesar_pago(self, total): # sin cuerpo real: cada hija lo implementa
        pass
```

**Nuestras 3 clases abstractas y sus contratos:**
- `Producto`: `calcular_precio()`, `esta_disponible(dia)`, `contar_platos()`
- `Pedido`: `calcular_cargos()`, `calcular_descuento()`, `obtener_tipo()`, `validar_para_preparar()`
- `Pago`: `calcular_monto()`, `procesar_pago(total)`, `acepta_delivery()`

`Producto("x", 10)`, `Pedido(None)` y `Pago("x")` lanzan `TypeError` (está en `pruebas.py`).

**Frase para la defensa:** "No existe un 'producto' suelto: o es plato, o bebida, o combo. Por eso Producto es abstracta y fija el contrato que las tres cumplen."

**Trampas:**
- Una clase abstracta SÍ puede tener constructor, atributos y métodos concretos (`Pedido` tiene casi toda la lógica de estados).
- Sin `ABC`, el decorador `@abstractmethod` no impide crear el objeto.
- `contiene_a()` es concreto en `Producto` porque tiene una respuesta válida por defecto (`self is producto`); `Combo` lo sobrescribe.

## 1.6 Relaciones del diagrama UML

| Relación | Símbolo | Significado | Ejemplo nuestro |
| --- | --- | --- | --- |
| Herencia | flecha con triángulo vacío | "es un" | `Plato` → `Producto` |
| Composición | rombo lleno | "es parte de y no existe sin el todo" | `Combo` ◆ `ComboProducto`; `Pedido` ◆ `PedidoProducto` |
| Agregación | rombo vacío | "agrupa objetos que existen solos" | `Restaurante` ◇ `Producto`, `Cliente`, `Pedido` |
| Asociación | flecha simple | "conoce a / tiene una referencia" | `Pedido` → `Cliente`, `Pedido` → `Pago` |
| Multiplicidad | `1`, `0..1`, `*`, `2..*` | cuántos objetos participan | Un combo tiene `2..*` líneas |

## 1.7 Python que hay que saber explicar
- `is` compara identidad (el mismo objeto); `==` compara valor. Usamos `is` para saber si un producto ya está en el pedido o en el combo.
- `round(x, 2)` deja el dinero en 2 decimales.
- `raise ValueError("...")` lanza el error; `try/except ValueError as error` en `main.py` lo atrapa y lo muestra sin cerrar el programa.
- Diccionario: `ZONAS = {"Cercado": 8, ...}` y `TRANSICIONES = {REGISTRADO: [EN_PREPARACION, CANCELADO], ...}`.
- `datetime.now()` da la fecha y hora; `.weekday()` da el número del día (0 = lunes) que usamos con `DIAS_SEMANA`.
- f-string: `f"Total: Bs {total:.2f}"` muestra 2 decimales.

---

# PARTE 2. PREGUNTAS POR PILAR (con respuesta)

## Abstracción
1. ¿Qué es una clase abstracta? → Una clase que no se puede instanciar y que define métodos que las hijas deben implementar.
2. ¿Cuáles son las nuestras y por qué? → Producto, Pedido y Pago: son conceptos generales, siempre se usa una hija concreta.
3. ¿Qué pasa con `Producto("x", 10)`? → `TypeError`, porque tiene métodos abstractos sin implementar.
4. ¿Qué pasa si `Plato` no implementa `contar_platos()`? → No se puede crear ningún Plato: `TypeError`.
5. ¿Qué pasa si quito `ABC` y dejo `@abstractmethod`? → Ya no se protege: se podría instanciar Producto.
6. ¿Una clase abstracta puede tener `__init__` y métodos normales? → Sí: Pedido tiene el constructor y toda la lógica de estados.
7. ¿Por qué `contiene_a` no es abstracto? → Tiene una respuesta correcta por defecto (`self is producto`); solo Combo necesita otra.
8. ¿Qué métodos abstractos tiene Pedido y por qué esos? → `calcular_cargos`, `calcular_descuento`, `obtener_tipo` y `validar_para_preparar`: son lo único que cambia entre local, para llevar y delivery.
9. ¿Para qué sirve `acepta_delivery()` abstracto? → Para que cada pago diga si vale en delivery, sin que el pedido pregunte su tipo.
10. ¿Dónde se prueba que las clases son abstractas? → En `pruebas.py`, con `try` / `assert False` / `except TypeError`.

## Herencia
1. ¿Qué es la herencia? → Una hija recibe los atributos y métodos del padre y agrega o cambia lo suyo ("es un").
2. ¿Cuántas subclases hay? → 9 (3 productos, 3 pedidos, 3 pagos).
3. ¿Qué hace `super().__init__(...)`? → Llama al constructor del padre para que inicialice y valide sus atributos.
4. ¿Qué pasa si una hija no llama a `super().__init__`? → Le faltan los atributos del padre y falla al usarlos.
5. ¿Por qué Bebida no tiene `_precio_vaso`? → Sería repetir el precio del padre; `precio_vaso` es una property que devuelve `precio`.
6. ¿Qué atributos heredan los pedidos? → `_numero`, `_cliente`, `_estado`, `_items`, `_fecha_hora`, `_dia`, `_pago`.
7. ¿Por qué Combo hereda de Producto? → Para que un combo pueda ir dentro de otro combo o de un pedido como cualquier producto.
8. ¿Qué es sobrescribir un método? → Que la hija defina un método con el mismo nombre que el padre para cambiar su comportamiento.
9. ¿Por qué `PedidoLocal` sobrescribe `ocupa_mesa` y los otros pedidos no? → Solo el local tiene mesa; los demás usan la versión del padre que devuelve False.
10. ¿Por qué el Combo valida "mínimo 2 productos" antes de `super().__init__`? → Para mostrar ese error y no uno de precio (sin productos la suma sería 0).

## Polimorfismo
1. ¿Qué es el polimorfismo? → El mismo método se comporta distinto según el objeto, y quien lo llama no necesita saber la clase.
2. Un ejemplo nuestro. → `calcular_precio()` en Plato, Bebida y Combo.
3. ¿Cómo calcula Combo su precio si dentro hay otro combo? → Llama a `calcular_precio()` de cada hijo; el combo hijo hace lo mismo con los suyos.
4. ¿Dónde hay `isinstance` o `if` por tipo? → En ningún lugar del modelo.
5. ¿Cómo evita Restaurante dos pedidos en la misma mesa sin isinstance? → Pregunta `ocupa_mesa(mesa)` a todos los pedidos; solo PedidoLocal puede responder True.
6. ¿Cómo sabe el delivery que la tarjeta no vale? → `puede_pagar_con(pago)` devuelve `pago.acepta_delivery()`, y la tarjeta responde False.
7. ¿Cómo agrupa el reporte por tipo? → Con `obtener_tipo()`, que cada pedido responde.
8. ¿Cómo se cuentan los envases dentro de un combo? → `contar_platos()`: plato 1, bebida 0, combo la suma de sus hijos por la cantidad.
9. ¿Qué tienes que tocar para agregar un Postre? → Solo crear la clase Postre con sus 3 métodos; Pedido, Combo y Restaurante no se tocan.
10. ¿El `if self._tipo == "jarra"` rompe el polimorfismo? → No: compara un valor dentro de la misma clase Bebida, no el tipo de la clase.
11. ¿Y los `if opcion == "1"` de main.py? → Tampoco: eligen la opción del menú que escribió el usuario.

## Encapsulación
1. ¿Qué es la encapsulación? → Proteger los datos del objeto y permitir cambiarlos solo por métodos o setters que validan.
2. ¿Qué diferencia hay entre `_x` y `__x`? → `_x` es protegido por convención; `__x` es privado y Python le cambia el nombre (`_Cliente__password`).
3. ¿Qué es `@property` y para qué el `@x.setter`? → La property permite leer `objeto.x`; el setter se ejecuta al asignar `objeto.x = valor` y valida.
4. ¿Por qué el constructor usa `self.precio = precio`? → Para pasar por el setter y validar al crear.
5. ¿Dónde se valida el precio > 0? → Solo en el setter de Producto, y sirve para las tres hijas.
6. ¿Por qué `items` devuelve `list(self._items)`? → Es una copia; si alguien la modifica, el pedido no cambia.
7. ¿Por qué `PedidoProducto.cantidad` no tiene setter? → Para que nadie cambie la cantidad con el pedido en preparación; se reemplaza el ítem.
8. ¿Por qué `password` no tiene property? → Es privado; solo se compara con `verificar_password(texto)`.
9. ¿Qué atributos son privados en el diagrama? → `correo` y `password` de Cliente.
10. ¿Por qué las reglas de la variante son `_descuento`, `_recargo`, etc. con property de solo lectura? → Para que estén en un solo lugar y nadie las cambie por accidente; cambiar una regla es cambiar una línea.
11. ¿Qué error se lanza cuando un dato es inválido? → `ValueError` con un mensaje claro; `main.py` lo atrapa y lo muestra.

---

# PARTE 3. PREGUNTAS POR MÓDULO

## Productos (`modelo/productos.py`)
1. ¿Qué devuelve `contar_platos()` de un combo con silpancho y mocochinchi? → 1.
2. ¿Por qué `dias_disponibles=None` y no `=DIAS_SEMANA` como valor por defecto? → Para no compartir la misma lista entre todos los platos; se crea una copia nueva.
3. ¿Qué pasa si escribo el día "Domingo"? → ValueError: los días van en minúscula y sin tildes.
4. ¿Cuánto cuesta una jarra de mocochinchi de Bs 6 el vaso? → 18 (3 vasos).
5. ¿Cuándo tiene descuento un combo? → Con 3 o más unidades: 15 %. Con 2 no hay descuento.
6. ¿Cómo detecta `contiene_a` un ciclo indirecto? → Busca en sus hijos y cada hijo combo busca en los suyos.
7. ¿Por qué `agregar_producto` pregunta `producto.contiene_a(self)`? → Si lo que agrego ya me contiene, agregarlo crearía un ciclo.
8. ¿Qué pasa si quito un producto y el combo queda con 1? → ValueError: mínimo 2.
9. `combo.precio` y `combo.calcular_precio()`, ¿son iguales? → No siempre: `precio` es la suma inicial; `calcular_precio()` calcula en vivo.
10. ¿Qué es `ComboProducto`? → La línea del combo: un producto y su cantidad (composición).

## Pedidos (`modelo/pedidos.py`)
1. ¿Qué estados hay y cuáles son las transiciones? → REGISTRADO → EN_PREPARACION → LISTO → ENTREGADO; CANCELADO solo desde REGISTRADO (diccionario `TRANSICIONES`).
2. ¿Por qué `cancelar()` llama a `cambiar_estado(CANCELADO)`? → Para que valide la transición; un pedido en preparación no se cancela.
3. ¿Qué se valida al pasar a EN_PREPARACION? → Que tenga al menos un ítem y `validar_para_preparar()` (delivery: subtotal ≥ 60).
4. ¿Cómo se calcula el total? → subtotal − descuento + cargos.
5. ¿Por qué el 5 % usa `contar_platos()` y no `len(items)`? → Porque cuenta platos (también dentro de combos) y por cantidad, no líneas.
6. ¿Qué pasa si agrego 20 silpanchos y después 1 más? → ValueError: el máximo es 20; la cantidad sigue en 20.
7. ¿Para qué sirve `_contador`? → Es de clase y da un número único a cada pedido.
8. ¿De dónde sale el día del pedido? → De la fecha actual (`weekday()`), o del parámetro `dia` para probar.
9. ¿Puede un pedido para llevar no tener cliente? → No, lanza ValueError (supuesto 8); el local sí puede.
10. ¿Qué valida `marcar_pagado`? → Que no esté pagado, que esté LISTO o ENTREGADO y que acepte ese pago.

## Pagos y clientes (`modelo/pagos.py`, `modelo/clientes.py`)
1. ¿Qué pasa si pago Bs 97 con Bs 50 en efectivo? → ValueError y el pedido no queda pagado.
2. ¿Cómo se calcula el cambio? → monto recibido − total.
3. ¿Por qué `cod_trans` y `celular` se guardan como texto? → Para validar dígitos y no perder ceros a la izquierda.
4. ¿Cuánto paga el cliente con tarjeta por un pedido de Bs 88,80? → Comisión 2,66; total 91,46.
5. ¿Por qué la tarjeta no se acepta en delivery? → Regla de la consigna; `acepta_delivery()` devuelve False.
6. ¿Cuándo se llenan `monto_base` y `fecha_hora`? → En `procesar_pago(total)`.
7. ¿Qué devuelve `procesar_pago`? → El texto del comprobante.
8. ¿Qué valida el setter de `celular`? → 8 dígitos y que empiece en 6 o 7.
9. ¿Cómo se comprueba un password si no se puede leer? → `verificar_password(texto)` devuelve True o False.
10. ¿Qué hace el `try/except` del setter de `monto_recibido`? → Convierte el texto a número; si no se puede, lanza ValueError con un mensaje claro.

## Restaurante y menú (`restaurante.py`, `main.py`)
1. ¿Qué es Restaurante? → El gestor: guarda el menú, los clientes y los pedidos (agregación).
2. ¿Qué valida `cobrar_pedido`? → Que el pedido exista, esté LISTO o ENTREGADO, no esté pagado y acepte ese pago.
3. ¿Por qué procesa el pago antes de marcarlo como pagado? → Si el pago falla (efectivo insuficiente), el pedido no queda pagado.
4. ¿Qué cuenta el reporte del día? → Solo pedidos pagados de hoy, agrupados por `obtener_tipo()`, con lo cobrado (incluye la comisión).
5. ¿Cómo saca el top 3 sin `sorted` ni `lambda`? → Cuenta unidades por producto y repite: busca el mayor, lo guarda y lo saca de la lista.
6. ¿Por qué no se puede registrar dos veces el mismo celular? → Porque el celular identifica al cliente en `buscar_cliente` (supuesto 5).
7. ¿Qué pasa en main.py si escribo letras donde va un número? → `int()` lanza ValueError, el `except` lo muestra y el menú sigue.
8. ¿Por qué main.py muestra `calcular_precio()` y no `precio`? → En un combo, `precio` no se actualiza; `calcular_precio()` sí.
9. ¿Qué datos de ejemplo se cargan al iniciar? → Silpancho, pique macho, chicharrón (domingo), sopa de maní, mocochinchi, Coca Cola, combo clásico y la cliente Ana (71234567).
10. ¿Dónde se atrapan los errores de validación? → En el `try/except ValueError` del `while` de `main()`.

---

# PARTE 4. TRAZAS (calcula a mano con la variante D)

| Pregunta | Cuenta | Resultado |
| --- | --- | --- |
| Combo silpancho 35 + mocochinchi 6 | 2 unidades, sin descuento | Bs 41,00 |
| Ese combo + sopa de maní 18 + jarra de mocochinchi 18 | (41 + 18 + 18) × 0,85 | Bs 65,45 |
| 2 silpanchos + 1 mocochinchi en un combo | (70 + 6) × 0,85 | Bs 64,60 |
| Delivery a Quillacollo con 2 combos clásicos | 82 + 15 | Bs 97,00 |
| Local con 6 silpanchos | 210 − 10,50 | Bs 199,50 |
| Local con 5 silpanchos | sin descuento | Bs 175,00 |
| Para llevar: 3 combos clásicos + 2 vasos de mocochinchi | 135 + envases 3 × 2 | Bs 141,00 |
| Delivery a Cercado con 1 silpancho | 35 < 60 | Error: mínimo Bs 60 |
| Pagar 141 con efectivo de 200 | 200 − 141 | Cambio Bs 59,00 |
| Pagar 199,50 con tarjeta | 199,50 + 3 % | Bs 205,48 (Python redondea 5,985 a 5,98) |

---

# PARTE 5. CAMBIOS EN VIVO (resumen; la tabla completa y probada está en `docs/guia_defensa.md`)

| Pedido del docente | Qué cambias |
| --- | --- |
| Otro descuento del combo | `Combo._descuento` en productos.py |
| Descuento desde 2 productos | `Combo._min_producto` |
| Quitar o cambiar el envase | `PedidoLlevar._costo_envase` en pedidos.py |
| Quitar o cambiar la comisión de tarjeta | `PagoTarjeta._recargo` en pagos.py |
| Quitar el cobro de envío | `PedidoDelivery.calcular_cargos`: `return 0` |
| Zona nueva o cambiar un envío | diccionario `PedidoDelivery.ZONAS` |
| Otro descuento local o desde otros platos | `PedidoLocal._desc_grupo` y `_platos_des` |
| Otro pedido mínimo | `PedidoDelivery._pedido_minimo` |
| Más mesas | `PedidoLocal._mesa_max` |
| Agregar un Postre | nueva clase hija de Producto con `calcular_precio`, `esta_disponible` y `contar_platos` (código en guia_defensa.md) |
| Nuevo método de pago | nueva clase hija de Pago con `calcular_monto`, `procesar_pago` y `acepta_delivery` |

Después de cada cambio: `python pruebas.py` y explicar qué prueba falla y por qué (o por qué falta una prueba si no falla ninguna).

---

# PARTE 6. ¿QUÉ PASA SI...?
- ¿... meto un combo dentro de sí mismo? → ValueError (ciclo directo); dentro de un combo que ya lo contiene → ValueError (ciclo indirecto).
- ¿... pido chicharrón el martes, o un combo que lo tiene? → ValueError: no está disponible.
- ¿... subo el precio del silpancho después de armar el combo? → El combo se actualiza solo con `calcular_precio()`.
- ¿... cancelo un pedido en preparación? → ValueError.
- ¿... agrego productos a un pedido LISTO? → ValueError: solo en REGISTRADO.
- ¿... cobro un pedido REGISTRADO, cancelado o ya pagado? → ValueError.
- ¿... pago con tarjeta un delivery? → ValueError y el pedido sigue sin pagar.
- ¿... abro dos pedidos en la mesa 5? → ValueError; al cancelarse o entregarse se libera.
- ¿... registro un celular que empieza en 5? → ValueError.
- ¿... creo un pedido para llevar sin cliente? → ValueError.

---

# PARTE 7. DIAGRAMA, VARIANTE Y PROCESO
1. ¿Qué cambió del diagrama v1 al v2? → Visibilidad y tipos; `max_producto` → `min_producto`; se quitó la herencia Cliente → Pago; se quitaron líneas que no tenían sentido; se agregó Restaurante y los métodos de la lógica.
2. ¿Dónde se relaciona Combo con Producto? → Herencia (Combo es un Producto) y composición Combo ◆ ComboProducto → Producto.
3. ¿Por qué la variante D no tiene envío gratis? → La tabla de la consigna dice "sin envío gratis".
4. ¿De dónde sale el 15 %? → Variante D, solo con 3 productos o más.
5. ¿Qué supuestos no consultaron? → Los 8 del acta, marcados con `# SUPUESTO:` en el código.
6. ¿Por qué no está la regla 9? → El docente indicó que no se incluye (está en el acta).
7. ¿Cómo trabajaron en equipo? → Ramas por módulo y Pull Request a main.
8. ¿Cómo usaron la IA? → Está en la bitácora de cada una; hay que responder con sinceridad y explicar el código.

---

# PARTE 8. PUNTOS DÉBILES QUE HAY QUE SABER RECONOCER
Si el docente los encuentra, se reconocen y se explica cómo se arreglan. Negarlos es peor.
1. **`ComboProducto.cantidad` todavía tiene setter público**: `combo.productos[0].cantidad = 50` cambia el combo desde fuera. En `PedidoProducto` ya se corrigió; en Combo se arregla igual (quitar el setter y reemplazar la línea).
2. **`combo.precio` no se actualiza**: guarda la suma inicial; el precio real es `calcular_precio()`.
3. **Redondeo de la tarjeta**: 199,50 × 3 % = 5,985; Python da 5,98 y a mano 5,99.
4. **Validación repetida**: `Pedido.agregar_producto` vuelve a validar la cantidad mínima aunque `PedidoProducto` ya lo hace; y Restaurante vuelve a validar el cliente que ya valida Pedido. No rompe nada, solo se repite.
5. **8 supuestos no consultados**: están declarados en el acta y en el código; se cambian en una línea si el docente dice otra cosa.

---

# PARTE 9. PLAN DE ESTUDIO
| Quién | Primero estudia | Después |
| --- | --- | --- |
| Yercko | Partes 1.4 y 1.5, Parte 3 de productos y restaurante | Postre en vivo y la traza del combo anidado |
| Maria Liz | Partes 1.2 y 1.3, Parte 3 de pedidos | Cambiar envase, descuento local y pedido mínimo en vivo |
| Anahi | Partes 1.2 y 1.5, Parte 3 de pagos, clientes y main | Nuevo método de pago y cambiar la comisión en vivo |
| Las tres | Partes 2, 4, 6 y 7 | Simulacro de 10 minutos con cronómetro, cambiando de rol |

Cada una debe poder explicar también el módulo de las otras: el docente puede preguntar cualquier fragmento.
