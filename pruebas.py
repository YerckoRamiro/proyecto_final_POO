from modelo.productos import Producto, Plato, Bebida, Combo
from modelo.pedidos import Pedido, PedidoLocal, PedidoLlevar, PedidoDelivery
from modelo.pagos import Pago, PagoEfectivo, PagoQr, PagoTarjeta
from modelo.clientes import Cliente


# ===== PRUEBAS DE PRODUCTOS ===== (Yercko)

# Producto es abstracta
try:
    Producto("prueba", 10)
    assert False, "Producto no deberia poder instanciarse"
except TypeError:
    pass

# Precio 0 o negativo y nombre vacio lanzan ValueError
try:
    Plato("Silpancho", 0)
    assert False, "precio 0 deberia fallar"
except ValueError:
    pass
try:
    Plato("Silpancho", -5)
    assert False, "precio negativo deberia fallar"
except ValueError:
    pass
try:
    Plato("   ", 35)
    assert False, "nombre vacio deberia fallar"
except ValueError:
    pass

# Plato: dias de venta (SUPUESTO 2: chicharron solo domingos)
silpancho = Plato("Silpancho", 35)
chicharron = Plato("Chicharron", 45, ["domingo"])
assert silpancho.esta_disponible("martes")
assert chicharron.esta_disponible("domingo")
assert not chicharron.esta_disponible("lunes")
assert silpancho.contar_platos() == 1
try:
    Plato("Chicharron", 45, ["Domingo"])
    assert False, "dia mal escrito deberia fallar"
except ValueError:
    pass

# Bebida: la jarra cuesta 3 vasos y no cuenta como plato
mocochinchi = Bebida("Mocochinchi", 6, "vaso", "refresco natural")
jarra_moco = Bebida("Mocochinchi", 6, "jarra", "refresco natural")
assert mocochinchi.calcular_precio() == 6
assert jarra_moco.calcular_precio() == 18
assert jarra_moco.contar_platos() == 0
assert jarra_moco.esta_disponible("lunes")
try:
    Bebida("Mocochinchi", 6, "botella", "refresco natural")
    assert False, "tipo invalido deberia fallar"
except ValueError:
    pass

# Caso de referencia variante D: silpancho 35 + mocochinchi 6 = Bs 41,00 (2 productos, sin descuento)
combo_clasico = Combo("Combo clasico", [silpancho, mocochinchi])
assert combo_clasico.calcular_precio() == 41.00

# Combo de 3 productos: 15 % -> (35 + 6 + 18) * 0.85 = 50,15
sopa = Plato("Sopa de mani", 18)
combo_completo = Combo("Combo completo", [silpancho, mocochinchi, sopa])
assert combo_completo.calcular_precio() == 50.15

# SUPUESTO 1: se cuentan unidades -> 2 silpanchos + 1 mocochinchi = 3 productos -> (70 + 6) * 0.85 = 64,60
combo_doble = Combo("Combo doble", [silpancho, mocochinchi])
combo_doble.agregar_producto(silpancho)
assert combo_doble.contar_productos() == 3
assert combo_doble.calcular_precio() == 64.60

# Combo que contiene otro combo: (41 + 45 + 18) * 0.85 = 88,40
pique = Plato("Pique macho", 45)
combo_grande = Combo("Combo grande", [combo_clasico, pique, sopa])
assert combo_grande.calcular_precio() == 88.40

# Envases: cuentan los platos dentro de combos, las bebidas no
assert combo_clasico.contar_platos() == 1
assert combo_grande.contar_platos() == 3

# Un combo esta disponible solo si todos sus productos lo estan
combo_domingo = Combo("Combo dominguero", [chicharron, mocochinchi])
assert combo_domingo.esta_disponible("domingo")
assert not combo_domingo.esta_disponible("martes")

# Cambiar el precio de un plato se refleja en los combos que lo contienen (tambien anidados)
silpancho.precio = 40
assert combo_clasico.calcular_precio() == 46.00
assert combo_grande.calcular_precio() == 92.65  # (46 + 45 + 18) * 0.85
silpancho.precio = 35

# Un combo no puede contenerse a si mismo, ni directa ni indirectamente
try:
    combo_clasico.agregar_producto(combo_clasico)
    assert False, "ciclo directo deberia fallar"
except ValueError:
    pass
try:
    combo_clasico.agregar_producto(combo_grande)
    assert False, "ciclo indirecto deberia fallar"
except ValueError:
    pass

# Minimo 2 productos al crear y al quitar
try:
    Combo("Solo uno", [silpancho])
    assert False, "combo de 1 producto deberia fallar"
except ValueError:
    pass
try:
    combo_clasico.quitar_producto(mocochinchi)
    assert False, "el combo no puede quedar con 1 producto"
except ValueError:
    pass

# La lista de productos del combo no se modifica desde fuera
copia = combo_clasico.productos
copia.clear()
assert combo_clasico.contar_productos() == 2


# ===== PRUEBAS DE PEDIDOS ===== (Maria Liz)

# Pedido es abstracta
try:
    Pedido(None)
    assert False, "Pedido no deberia poder instanciarse"
except TypeError:
    pass


# ===== PRUEBAS DE PAGOS Y CLIENTES ===== (Anahi)

# Pago es abstracta
try:
    Pago("prueba")
    assert False, "Pago no deberia poder instanciarse"
except TypeError:
    pass


# ===== PRUEBAS DE RESTAURANTE ===== (integracion)


print("Todas las pruebas pasaron")
