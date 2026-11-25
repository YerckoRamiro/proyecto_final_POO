# Registro de uso de IA

- **Estudiante:** Maria Liz Quispe Mamani
- **Proyecto:** Sistema de pedidos "Sabor Valluno"
- **Variante:** D
- **Semana:** 4

| N.º | Fecha | Herramienta | Tipo de uso | Consulta textual | Qué acepté | Qué modifiqué y por qué | Archivo o clase | ¿Lo explico sin ayuda? |
| 1 | 24/11/2026 | Gemini | Generación de código | "Pasé CLAUDE.md, pedidos.py y productos.py para implementar la clase PedidoProducto paso a paso." | La validación de cantidad (1 a 20) en el setter y los métodos calcular_precio() y contar_platos() delegando al producto. | [Completa si cambiaste algo o "Ninguna"] | modelo/pedidos.py, PedidoProducto | [Sí / Parcial / No] |
| 2 | 24/11/2026 | Gemini | Generación de código | "Continuamos con la clase abstracta Pedido en modelo/pedidos.py." | La implementación de agregar_producto, quitar_producto, cálculos de subtotal/total, control de TRANSICIONES y métodos de estado y pago. | [Completa si cambiaste algo o "Ninguna"] | modelo/pedidos.py, Pedido | [Sí / Parcial / No] |
| 3 | 24/11/2026 | Gemini | Generación de código | "Sigamos con PedidoLocal en modelo/pedidos.py." | Validación de mesa (1 a 15), descuento del 5 % con 6 o más platos (variante D), cargos en 0 y sobrescritura de ocupa_mesa(). | [Completa si cambiaste algo o "Ninguna"] | modelo/pedidos.py, PedidoLocal | [Sí / Parcial / No] |
| 4 | 24/11/2026 | Gemini | Generación de código | "Sigamos con PedidoLlevar en modelo/pedidos.py." | Cálculo de envases con contar_platos() * _costo_envase (Bs 2 por plato), descuento en 0 y métodos abstractos de Pedido. | [Completa si cambiaste algo o "Ninguna"] | modelo/pedidos.py, PedidoLlevar | [Sí / Parcial / No] |
| 5 | 24/11/2026 | Gemini | Generación de código | "Sigamos con PedidoDelivery en modelo/pedidos.py." | Validación de zona y dirección, costo fijo por zona sin envío gratis, pedido mínimo de Bs 60 en validar_para_preparar() y puede_pagar_con() polimórfico. | [Completa si cambiaste algo o "Ninguna"] | modelo/pedidos.py, PedidoDelivery | [Sí / Parcial / No] |
| 6 | 25/11/2026 | Gemini | Revisión y corrección | "Necesito corregir un hueco de encapsulación... [pegado código de modelo/pedidos.py]" | Eliminación del setter de cantidad en PedidoProducto, reemplazo de ítem al sumar, validación de dia y estado al pagar, f-strings con constantes y líneas en blanco entre clases. | [Completa si ajustaste algo o "Ninguna"] | modelo/pedidos.py | [Sí / Parcial / No] |

## Declaración

Declaro que este registro refleja de forma honesta todos los usos de herramientas de inteligencia artificial que hice en el proyecto, y que puedo explicar sin ayuda el código que entrego, salvo donde lo indico en la última columna.

Firma: ______________________ Fecha: ____________
