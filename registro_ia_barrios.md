# Registro de uso de IA

- **Estudiante:** Anahi Mishele Barrios Choquetarqui
- **Proyecto:** Sistema de pedidos "Sabor Valluno"
- **Variante:** D
- **Semana:** 4

| N.º | Fecha | Herramienta | Tipo de uso | Consulta textual | Qué acepté | Qué modifiqué y por qué | Archivo o clase | ¿Lo explico sin ayuda? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
1 Grok Revisión y mejora de código	Escribí yo la clase Cliente y se la envié a la IA para que verificara si servía y la corrigiera	La mejora de usar @property (con su setter) y la explicación de para qué sirve: leer el atributo de forma normal pero validando el dato al guardarlo	Mantuve la lógica que yo había escrito y agregué los @property que me sugirió la IA	modelo/clientes.py, clase Cliente	Parcialmente: entiendo para qué sirve @property, pero no recuerdo todos los detalles de la explicación
2 Grok 	Revisión de código	Envié el esqueleto de Pago, PagoEfectivo, PagoQr y PagoTarjeta para ver si estaba bien	La sugerencia de usar ABC y @abstractmethod para que Pago sea una clase abstracta. Me dijo que el resto estaba bien por ahora, porque el código se une con el trabajo del equipo	No cambié más, porque los métodos con pass los completo en el Bloque 1. No recuerdo el detalle exacto de la explicación que me dio	modelo/pagos.py, clase Pago y sus hijas	Parcialmente: sé que Pago es abstracta y que las hijas deben implementar sus métodos
3 Grok Revisión de pruebas	Envié mi prueba de que Pago es abstracta, escrita como función con def, y pedí que la revisara	Cambiar la prueba al formato try / assert False / except TypeError, igual que el resto de pruebas.py. Los from ... import ya venían en el esqueleto	Ajusté mi prueba al mismo formato que las demás	pruebas.py, sección PRUEBAS DE PAGOS Y CLIENTES	Sí
| 4 | 24/11/2026 | Claude | Completar código | Le envié el esqueleto de Cliente y le pedí que completara los setters de nombre y celular | Validación del nombre (no vacío) y del celular (8 dígitos que empiezan en 6 o 7) con ValueError | [Lo que cambies tú, o "ninguno"] | modelo/clientes.py, clase Cliente | [Sí / Parcialmente] |
| 5 | 25/11/2026 | Claude | Completar código | Le envié el esqueleto de Pago y sus clases hijas y le pedí que completara los pass | Validaciones, cálculo del cambio, comisión del 3%, comprobantes y acepta_delivery | [Lo que cambies tú, o "ninguno"] | modelo/pagos.py | [Sí / Parcialmente] |
## Declaración

Declaro que este registro refleja de forma honesta todos los usos de herramientas de inteligencia artificial que hice en el proyecto, y que puedo explicar sin ayuda el código que entrego, salvo donde lo indico en la última columna(pero aun asi no confie en mi memoria ya que soy muy olvidadiza).

Firma: ______________________ Fecha: ____________
