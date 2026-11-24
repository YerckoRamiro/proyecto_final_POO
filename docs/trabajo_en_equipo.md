# Plan de trabajo en equipo – noche del 24/11/2026

## Responsables

| Responsable | Rama | Archivos |
| --- | --- | --- |
| Yercko | `feature/productos` | `modelo/productos.py` + sección PRODUCTOS de `pruebas.py` |
| Maria Liz | `feature/pedidos` | `modelo/pedidos.py` + sección PEDIDOS de `pruebas.py` |
| Anahi | `feature/pagos-clientes` | `modelo/pagos.py`, `modelo/clientes.py` + sección PAGOS Y CLIENTES de `pruebas.py` |
| Yercko y Anahi | `feature/integracion` | `restaurante.py` (Yercko), `main.py` (Anahi) |
| Maria Liz | `feature/integracion` | `README.md`, diagrama v2 desde el código |

Regla: cada quien toca solo sus archivos. Si necesitas cambiar un archivo ajeno, avisa en el grupo en lugar de editarlo.

## Bloque 0 (30 min) – Arranque

Yercko sube el esqueleto a `main`. Maria Liz y Anahi hacen `git pull` y configuran su usuario de Git.

- [ ] Yercko: commit y `git push` del esqueleto en `main`
- [ ] Maria Liz: `git pull`, `git config user.name` y `user.email` con sus datos
- [ ] Anahi: `git pull`, `git config user.name` y `user.email` con sus datos
- [ ] Las tres corren `python pruebas.py` y ven "Todas las pruebas pasaron"
- [ ] Cada una crea su rama

## Bloque 1 (60–90 min) – Cada quien su módulo, en paralelo

- Yercko: `modelo/productos.py` (Producto, Plato, Bebida, ComboProducto, Combo)
- Maria Liz: `modelo/pedidos.py` (PedidoProducto, Pedido, PedidoLocal, PedidoLlevar, PedidoDelivery)
- Anahi: `modelo/pagos.py` (Pago, PagoEfectivo, PagoQr, PagoTarjeta) y `modelo/clientes.py` (Cliente)

Lista de verificación (cada una):
- [ ] Todos los `pass` de mis clases reemplazados por lógica
- [ ] Setters con validación que lanzan `ValueError` con mensaje claro
- [ ] Sin `isinstance`, `type()`, lambdas ni comprensiones de lista
- [ ] Dinero con `round(x, 2)`
- [ ] Mis pruebas escritas en mi sección de `pruebas.py` y `python pruebas.py` pasa
- [ ] Commits pequeños, en español e imperativo, con mi propio usuario
- [ ] Entrada nueva en mi `docs/registro_ia_<apellido>.md`
- [ ] Puedo explicar cada método sin mirar el código

## Bloque 2 (45 min) – Pull Requests cruzados e integración

| Pull Request | Revisa |
| --- | --- |
| `feature/productos` | Anahi |
| `feature/pedidos` | Yercko |
| `feature/pagos-clientes` | Maria Liz |

Orden de unión a `main`: productos → pagos/clientes → pedidos.
Luego, en `feature/integracion`: Yercko hace `restaurante.py` y Anahi hace `main.py`. Maria Liz prepara el README y empieza el diagrama v2 desde el código.

- [ ] Cada PR tiene al menos un comentario real del revisor
- [ ] `python pruebas.py` pasa antes de unir cada PR
- [ ] Los PR se unieron en el orden acordado
- [ ] Después de cada unión, todas hacen `git pull` en `main`
- [ ] Rama `feature/integracion` creada desde `main` actualizado

## Bloque 3 (30–45 min) – Cierre técnico

- [ ] `pruebas.py` completo (mínimo 8 casos, objetivo ~15, incluido el caso de referencia: silpancho 35 + mocochinchi 6 = Bs 41,00)
- [ ] Auditoría: nombres iguales al diagrama, `# SUPUESTO:` en las 4 constantes, sin construcciones prohibidas, sin código muerto
- [ ] Diagrama v2 igual al código (clases, atributos, métodos y constantes)
- [ ] Bitácoras de IA de las tres al día
- [ ] Acta de consultas al día (completar las filas PENDIENTE)
- [ ] PR de `feature/integracion` revisado y unido

## Bloque 4 (60 min) – Estudio cruzado y simulacro de defensa

Cada una explica su módulo a las otras en 10 minutos. Luego simulan la defensa con cronómetro: una hace de docente, elige un fragmento, pide un cambio en vivo y pregunta "¿qué pasa si...?".

- [ ] Yercko explicó productos (Combo, `contiene_a`, precio del combo)
- [ ] Maria Liz explicó pedidos (estados, transiciones, cargos y descuentos)
- [ ] Anahi explicó pagos y clientes (`acepta_delivery`, comisión, validación del celular)
- [ ] Cada una respondió al menos 3 preguntas sobre un módulo que NO escribió
- [ ] Cada una hizo un cambio en vivo (por ejemplo, cambiar una constante `# SUPUESTO:`) y corrió `pruebas.py`

## Comandos para empezar (Maria Liz y Anahi)

Si ya tienen el repositorio clonado:

```
cd proyecto_final_POO
git checkout main
git pull
```

Si no lo tienen:

```
git clone https://github.com/YerckoRamiro/proyecto_final_POO.git
cd proyecto_final_POO
```

Configurar el usuario (cada una con sus propios datos, solo en este repositorio):

```
git config user.name "Nombre Apellido"
git config user.email "correo-de-su-cuenta-github"
git config user.name
```

Crear la rama:

```
git checkout -b feature/pedidos            # Maria Liz
git checkout -b feature/pagos-clientes     # Anahi
```

Al terminar el bloque 1:

```
python pruebas.py
git add modelo/pedidos.py pruebas.py docs/registro_ia_quispe.md
git commit -m "Implementa estados y transiciones de Pedido"
git push -u origin feature/pedidos
```

(Anahi lo mismo con sus archivos y su rama.) Después abren el Pull Request en GitHub hacia `main`.
