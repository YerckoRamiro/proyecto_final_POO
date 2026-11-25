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

## Cambios respecto al diagrama v1 (aprobado)

1. Visibilidad unificada: atributos protegidos `#` con property (regla de encapsulación); `correo` y `password` de `Cliente` privados `-`.
2. `Combo.max_producto` → `min_producto`: en la variante D es el **mínimo** de productos (3) para el 15 % de descuento.
3. Se quita la herencia `Cliente → Pago` (un cliente no es un pago). `Pedido` se asocia con `Cliente` y con `Pago`.
4. Se quitan las líneas `ComboProducto — Pedido` y `PagoQr — Cliente` (el pedido usa `PedidoProducto`; el pago se asocia al pedido).
5. `PedidoProducto` agrega `cantidad` (1 a 20).
6. Se agregan los atributos y métodos que necesita la lógica (estados, `calcular_total`, `acepta_delivery`, etc.) y la clase `Restaurante` (gestor).
7. `Bebida` agrega `categoria`; `PedidoDelivery` agrega `zona` y `ZONAS`; `Cliente` agrega `verificar_password()`.

## Diagrama

```mermaid
classDiagram
    direction TB

    note "+ publico | # protegido (_x en Python, con @property) | - privado (__x en Python)\nsubrayado = atributo de clase (static) | cursiva = abstracto"

    class Producto {
        <<abstract>>
        #nombre
        #precio
        +calcular_precio()*
        +esta_disponible(dia)*
        +contar_platos()*
        +contiene_a(producto)
    }

    class Plato {
        #dias_disponibles
        +calcular_precio()
        +esta_disponible(dia)
        +contar_platos()
    }

    class Bebida {
        +VASOS_POR_JARRA$
        #tipo
        #categoria
        +precio_vaso
        +calcular_vaso()
        +calcular_precio()
        +esta_disponible(dia)
        +contar_platos()
    }

    class Combo {
        +MIN_PRODUCTOS$
        #min_producto$
        #descuento$
        #productos
        +agregar_producto(producto, cantidad)
        +quitar_producto(producto)
        +contar_productos()
        +calcular_precio()
        +esta_disponible(dia)
        +contar_platos()
        +contiene_a(producto)
    }

    class ComboProducto {
        #producto
        #cantidad
        +calcular_precio()
        +contar_platos()
    }

    class Pedido {
        <<abstract>>
        +REGISTRADO$
        +EN_PREPARACION$
        +LISTO$
        +ENTREGADO$
        +CANCELADO$
        +TRANSICIONES$
        #contador$
        #numero
        #cliente
        #estado
        #items
        #fecha_hora
        #dia
        #pago
        +agregar_producto(producto, cantidad)
        +quitar_producto(producto)
        +calcular_subtotal()
        +contar_platos()
        +calcular_total()
        +cambiar_estado(nuevo)
        +cancelar()
        +esta_abierto()
        +ocupa_mesa(mesa)
        +puede_pagar_con(pago)
        +marcar_pagado(pago)
        +esta_pagado()
        +calcular_cargos()*
        +calcular_descuento()*
        +obtener_tipo()*
        +validar_para_preparar()*
    }

    class PedidoProducto {
        +CANTIDAD_MIN$
        +CANTIDAD_MAX$
        #pedido
        #producto
        #cantidad
        +calcular_precio()
        +contar_platos()
    }

    class PedidoLocal {
        #mesa_min$
        #mesa_max$
        #platos_des$
        #desc_grupo$
        #mesa
        +calcular_cargos()
        +calcular_descuento()
        +obtener_tipo()
        +validar_para_preparar()
        +ocupa_mesa(mesa)
    }

    class PedidoLlevar {
        #costo_envase$
        +calcular_cargos()
        +calcular_descuento()
        +obtener_tipo()
        +validar_para_preparar()
    }

    class PedidoDelivery {
        +ZONAS$
        #pedido_minimo$
        #zona
        #direccion_ent
        +calcular_cargos()
        +calcular_descuento()
        +obtener_tipo()
        +validar_para_preparar()
        +puede_pagar_con(pago)
    }

    class Pago {
        <<abstract>>
        #nombre
        #monto_base
        #fecha_hora
        +calcular_monto()*
        +procesar_pago(total)*
        +acepta_delivery()*
    }

    class PagoEfectivo {
        #monto_recibido
        #cambio
        +calcular_cambio()
        +calcular_monto()
        +procesar_pago(total)
        +acepta_delivery()
    }

    class PagoQr {
        +LARGO_CODIGO$
        #cod_trans
        +calcular_monto()
        +procesar_pago(total)
        +acepta_delivery()
    }

    class PagoTarjeta {
        #recargo$
        +calcular_comision()
        +calcular_monto()
        +procesar_pago(total)
        +acepta_delivery()
    }

    class Cliente {
        #nombre
        #celular
        -correo
        -password
        #direccion
        +verificar_password(texto)
    }

    class Restaurante {
        #menu
        #clientes
        #pedidos
        +registrar_producto(producto)
        +armar_combo(nombre, productos)
        +listar_menu(dia)
        +registrar_cliente(nombre, celular, correo, password, direccion)
        +buscar_cliente(celular)
        +crear_pedido_local(mesa)
        +crear_pedido_para_llevar(cliente)
        +crear_pedido_delivery(cliente, zona, direccion_ent)
        +buscar_pedido(numero)
        +cobrar_pedido(numero, pago)
        +reporte_ventas_dia()
        +top_productos(cantidad)
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
