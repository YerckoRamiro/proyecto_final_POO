# Diagrama de clases v2 (generado desde el código)

Fuente de verdad: el código. Si cambia una clase, se actualiza este diagrama en el mismo commit.
GitHub dibuja el diagrama automáticamente. Para exportarlo a PNG: copiar el bloque en https://mermaid.live y descargar.

## Leyenda

| Símbolo | Significado | En Python |
| --- | --- | --- |
| `+` | público | métodos, properties y constantes en MAYÚSCULAS |
| `#` | protegido | `self._nombre`, se lee con `@property nombre` (si tiene setter, el setter valida) |
| `-` | privado | `self.__nombre` (name mangling); solo la propia clase lo usa |
| subrayado (`$`) | atributo de clase (static) | definido en la clase, compartido por todos los objetos |
| cursiva (`*`) / `<<abstract>>` | abstracto | `ABC` y `@abstractmethod` |
| `nombre: tipo` / `metodo() tipo` | tipo del atributo / tipo que devuelve el método | solo en el diagrama (el código no usa anotaciones de tipo) |
| `*--` rombo lleno | composición: la parte no existe sin el todo | `Combo` crea sus `ComboProducto`; `Pedido` crea sus `PedidoProducto` |
| `o--` rombo vacío | agregación: el gestor agrupa objetos que existen por sí solos | `Restaurante` guarda productos, clientes y pedidos |
| `-->` flecha | asociación: guarda una referencia a otro objeto | `Pedido` → `Cliente`, `Pedido` → `Pago` |

## Cambios respecto al diagrama v1 (aprobado)

1. Visibilidad unificada: atributos protegidos `#` con property (regla de encapsulación); `correo` y `password` de `Cliente` privados `-`.
2. Se agregan los tipos de todos los atributos y lo que devuelve cada método.
3. `Combo.max_producto` → `min_producto`: en la variante D es el **mínimo** de productos (3) para el 15 % de descuento.
4. Se quita la herencia `Cliente → Pago` (un cliente no es un pago). `Pedido` se asocia con `Cliente` y con `Pago`.
5. Se quitan las líneas `ComboProducto — Pedido` y `PagoQr — Cliente` (el pedido usa `PedidoProducto`; el pago se asocia al pedido).
6. `PedidoProducto` agrega `cantidad` (1 a 20). `Combo` agrega `contar_productos()` (suma unidades para el descuento).
7. Se agregan los atributos y métodos que necesita la lógica (estados, `calcular_total`, `acepta_delivery`, etc.) y la clase `Restaurante` (gestor).
8. `Bebida` agrega `categoria`; `PedidoDelivery` agrega `zona` y `ZONAS`; `Cliente` agrega `verificar_password()`.

## Diagrama

```mermaid
classDiagram
    direction TB

    note "+ publico | # protegido (_x) | - privado (__x) | subrayado = de clase | cursiva = abstracto\nCAMBIOS v1 -> v2: 1) visibilidad y tipos  2) max_producto -> min_producto (variante D: minimo 3)\n3) se quita la herencia Cliente -> Pago  4) se quitan ComboProducto-Pedido y PagoQr-Cliente\n5) PedidoProducto + cantidad, Combo + contar_productos()  6) se agrega Restaurante y los metodos de la logica\n7) Bebida + categoria, PedidoDelivery + zona y ZONAS, Cliente + verificar_password()"

    class Producto {
        <<abstract>>
        #nombre: str
        #precio: float
        +calcular_precio() float*
        +esta_disponible(dia: str) bool*
        +contar_platos() int*
        +contiene_a(producto: Producto) bool
    }

    class Plato {
        #dias_disponibles: list~str~
        +calcular_precio() float
        +esta_disponible(dia: str) bool
        +contar_platos() int
    }

    class Bebida {
        +VASOS_POR_JARRA: int$
        #tipo: str
        #categoria: str
        +precio_vaso: float
        +calcular_vaso() int
        +calcular_precio() float
        +esta_disponible(dia: str) bool
        +contar_platos() int
    }

    class Combo {
        +MIN_PRODUCTOS: int$
        #min_producto: int$
        #descuento: float$
        #productos: list~ComboProducto~
        +agregar_producto(producto: Producto, cantidad: int) None
        +quitar_producto(producto: Producto) None
        +contar_productos() int
        +calcular_precio() float
        +esta_disponible(dia: str) bool
        +contar_platos() int
        +contiene_a(producto: Producto) bool
    }

    class ComboProducto {
        #producto: Producto
        #cantidad: int
        +calcular_precio() float
        +contar_platos() int
    }

    class Pedido {
        <<abstract>>
        +REGISTRADO: str$
        +EN_PREPARACION: str$
        +LISTO: str$
        +ENTREGADO: str$
        +CANCELADO: str$
        +TRANSICIONES: dict$
        #contador: int$
        #numero: int
        #cliente: Cliente
        #estado: str
        #items: list~PedidoProducto~
        #fecha_hora: datetime
        #dia: str
        #pago: Pago
        +agregar_producto(producto: Producto, cantidad: int) None
        +quitar_producto(producto: Producto) None
        +calcular_subtotal() float
        +contar_platos() int
        +calcular_total() float
        +cambiar_estado(nuevo: str) None
        +cancelar() None
        +esta_abierto() bool
        +ocupa_mesa(mesa: int) bool
        +puede_pagar_con(pago: Pago) bool
        +marcar_pagado(pago: Pago) None
        +esta_pagado() bool
        +calcular_cargos() float*
        +calcular_descuento() float*
        +obtener_tipo() str*
        +validar_para_preparar() None*
    }

    class PedidoProducto {
        +CANTIDAD_MIN: int$
        +CANTIDAD_MAX: int$
        #pedido: Pedido
        #producto: Producto
        #cantidad: int
        +calcular_precio() float
        +contar_platos() int
    }

    class PedidoLocal {
        #mesa_min: int$
        #mesa_max: int$
        #platos_des: int$
        #desc_grupo: float$
        #mesa: int
        +calcular_cargos() float
        +calcular_descuento() float
        +obtener_tipo() str
        +validar_para_preparar() None
        +ocupa_mesa(mesa: int) bool
    }

    class PedidoLlevar {
        #costo_envase: float$
        +calcular_cargos() float
        +calcular_descuento() float
        +obtener_tipo() str
        +validar_para_preparar() None
    }

    class PedidoDelivery {
        +ZONAS: dict$
        #pedido_minimo: float$
        #zona: str
        #direccion_ent: str
        +calcular_cargos() float
        +calcular_descuento() float
        +obtener_tipo() str
        +validar_para_preparar() None
        +puede_pagar_con(pago: Pago) bool
    }

    class Pago {
        <<abstract>>
        #nombre: str
        #monto_base: float
        #fecha_hora: datetime
        +calcular_monto() float*
        +procesar_pago(total: float) str*
        +acepta_delivery() bool*
    }

    class PagoEfectivo {
        #monto_recibido: float
        #cambio: float
        +calcular_cambio() float
        +calcular_monto() float
        +procesar_pago(total: float) str
        +acepta_delivery() bool
    }

    class PagoQr {
        +LARGO_CODIGO: int$
        #cod_trans: str
        +calcular_monto() float
        +procesar_pago(total: float) str
        +acepta_delivery() bool
    }

    class PagoTarjeta {
        #recargo: float$
        +calcular_comision() float
        +calcular_monto() float
        +procesar_pago(total: float) str
        +acepta_delivery() bool
    }

    class Cliente {
        #nombre: str
        #celular: str
        -correo: str
        -password: str
        #direccion: str
        +verificar_password(texto: str) bool
    }

    class Restaurante {
        #menu: list~Producto~
        #clientes: list~Cliente~
        #pedidos: list~Pedido~
        +registrar_producto(producto: Producto) None
        +armar_combo(nombre: str, productos: list) Combo
        +listar_menu(dia: str) list
        +registrar_cliente(nombre: str, celular: str, correo: str, password: str, direccion: str) Cliente
        +buscar_cliente(celular: str) Cliente
        +crear_pedido_local(mesa: int) PedidoLocal
        +crear_pedido_para_llevar(cliente: Cliente) PedidoLlevar
        +crear_pedido_delivery(cliente: Cliente, zona: str, direccion_ent: str) PedidoDelivery
        +buscar_pedido(numero: int) Pedido
        +cobrar_pedido(numero: int, pago: Pago) str
        +reporte_ventas_dia() dict
        +top_productos(cantidad: int) list
    }

    Producto <|-- Plato
    Producto <|-- Bebida
    Producto <|-- Combo
    Combo "1" *-- "2..*" ComboProducto : contiene
    ComboProducto "*" --> "1" Producto

    Pedido <|-- PedidoLocal
    Pedido <|-- PedidoLlevar
    Pedido <|-- PedidoDelivery
    Pedido "1" *-- "0..*" PedidoProducto : items
    PedidoProducto "*" --> "1" Producto
    Pedido "*" --> "0..1" Cliente : cliente
    Pedido "1" --> "0..1" Pago : pago

    Pago <|-- PagoEfectivo
    Pago <|-- PagoQr
    Pago <|-- PagoTarjeta

    Restaurante "1" o-- "*" Producto : menu
    Restaurante "1" o-- "*" Cliente : clientes
    Restaurante "1" o-- "*" Pedido : pedidos
```
