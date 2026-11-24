# Registro de uso de IA

- **Estudiante:** Yercko Ramiro Nina Gomez
- **Proyecto:** Sistema de pedidos "Sabor Valluno"
- **Variante:** D
- **Semana:** 4

| N.º | Fecha | Herramienta | Tipo de uso | Consulta textual | Qué acepté | Qué modifiqué y por qué | Archivo o clase | ¿Lo explico sin ayuda? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 24/11/2026 | Claude Code | Análisis del código existente, planificación y generación del esqueleto | "Lee CLAUDE.md completo. Esta es la sesión de arranque [...] Entrégame un informe corto [...] Después de mi OK: crea el esqueleto del modelo [...] crea docs/acta_consultas.md [...] los tres registros de IA [...] docs/trabajo_en_equipo.md [...] haz un commit en main". Respuesta al informe: "OK, 1 quiero que coincida el diagrama final con el codigo. Aplica los nombres del diagrama png [...], 2 sí, opción 1, 4 sí" | Informe de diferencias entre el código, CLAUDE.md y el diagrama; opción 1 para el precio del Combo; esqueleto de las clases en `modelo/` con los nombres del diagrama; acta, bitácoras y plan de trabajo | (completar) | `modelo/productos.py`, `modelo/pedidos.py`, `modelo/pagos.py`, `modelo/clientes.py`, `restaurante.py`, `main.py`, `pruebas.py`, `docs/` | (completar) |
| 2 | 24/11/2026 | Claude Code | Corrección del esqueleto para que coincida con el diagrama y creación del diagrama v2 | "Estas tomando en cuentas que todo el codigo debe coincidir con el diagrama? [...] estrictamente lo que hay en el diagrama tiene que estar en el codigo. de igual manera no te olvides del poliformismo la encapsulacion y herencia" / "igual en el diagrama agrega que tipo de atributo es privado publico protegido etc. [...] Si corrige todo eso pero que en el diagrama hay que cambiar." | Nombres exactos del diagrama con atributo protegido y property; `correo` y `password` privados en Cliente; `max_producto` → `min_producto`; quitar la herencia Cliente → Pago; diagrama v2 en Mermaid con visibilidad | (completar) | `modelo/*.py`, `restaurante.py`, `Diagramas/diagrama_v2.md` | (completar) |

## Declaración

Declaro que este registro refleja de forma honesta todos los usos de herramientas de inteligencia artificial que hice en el proyecto, y que puedo explicar sin ayuda el código que entrego, salvo donde lo indico en la última columna.

Firma: ______________________ Fecha: ____________
