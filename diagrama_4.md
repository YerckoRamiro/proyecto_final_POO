# Diagrama de clases v2 – Pagos y Clientes (generado desde el código)

Fuente de verdad: el código de `modelo/pagos.py` y `modelo/clientes.py`. Si cambia una clase, se actualiza este diagrama en el mismo commit.
GitHub dibuja el diagrama automáticamente. Para exportarlo a PNG: copiar el bloque en https://mermaid.live y descargar.

## Leyenda

| Símbolo | Significado | En Python |
| --- | --- | --- |
| `+` | público | métodos, properties y constantes en MAYÚSCULAS |
| `#` | protegido | `self._nombre`, se lee con `@property nombre` (si tiene setter, el setter valida) |
| `-` | privado | `self.__nombre` (name mangling); solo la propia clase lo usa |
| subrayado (`$`) | atributo de clase (static) | definido en la clase, compartido por todos los objetos |
| cursiva (`*`) / `<<abstract>>` | abstracto | `ABC` y `@abstractmethod` |

## Diagrama

```mermaid
classDiagram
    direction TB

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

    class Pedido {
        <<abstract>>
    }

    Pago <|-- PagoEfectivo
    Pago <|-- PagoQr
    Pago <|-- PagoTarjeta

    Pedido "*" --> "0..1" Cliente : cliente
    Pedido "1" --> "0..1" Pago : pago
```

`Pedido` aparece vacío solo para mostrar con qué se asocian `Cliente` y `Pago`; sus atributos y métodos están en el diagrama del módulo de pedidos.