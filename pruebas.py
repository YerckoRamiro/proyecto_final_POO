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
from restaurante import Restaurante

restaurante = Restaurante()
r_silpancho = Plato("Silpancho", 35)
r_chicharron = Plato("Chicharron", 45, ["domingo"])
r_moco = Bebida("Mocochinchi", 6, "vaso", "refresco natural")
restaurante.registrar_producto(r_silpancho)
restaurante.registrar_producto(r_chicharron)
restaurante.registrar_producto(r_moco)

# armar_combo crea el combo y lo agrega al menu
r_combo = restaurante.armar_combo("Combo clasico", [r_silpancho, r_moco])
assert r_combo.calcular_precio() == 41.00
assert len(restaurante.menu) == 4

# listar_menu: el chicharron (y un combo con chicharron) solo aparece el domingo
r_combo_domingo = restaurante.armar_combo("Combo dominguero", [r_chicharron, r_moco])
assert len(restaurante.listar_menu("domingo")) == 5
martes = restaurante.listar_menu("martes")
assert len(martes) == 3
assert r_chicharron not in martes
assert r_combo_domingo not in martes
try:
    restaurante.listar_menu("Domingo")
    assert False, "dia mal escrito deberia fallar"
except ValueError:
    pass

# el menu no se modifica desde fuera
restaurante.menu.clear()
assert len(restaurante.menu) == 5

# registrar y buscar clientes por celular
r_ana = restaurante.registrar_cliente("Ana", "71234567", "ana@correo.com", "clave", "Calle Sucre 10")
assert restaurante.buscar_cliente("71234567") is r_ana
try:
    restaurante.registrar_cliente("Otra", "71234567", "otra@correo.com", "x", "Calle 2")
    assert False, "celular repetido deberia fallar"
except ValueError:
    pass
try:
    restaurante.buscar_cliente("69999999")
    assert False, "cliente inexistente deberia fallar"
except ValueError:
    pass

# crear pedidos de los tres tipos y buscarlos por numero
r_local = restaurante.crear_pedido_local(5)
r_llevar = restaurante.crear_pedido_para_llevar(r_ana)
r_delivery = restaurante.crear_pedido_delivery(r_ana, "Quillacollo", "Av. Blanco Galindo km 5")
assert restaurante.buscar_pedido(r_llevar.numero) is r_llevar
assert len(restaurante.pedidos) == 3
try:
    restaurante.buscar_pedido(9999)
    assert False, "pedido inexistente deberia fallar"
except ValueError:
    pass

# una mesa no puede tener dos pedidos abiertos (ocupa_mesa, sin isinstance)
try:
    restaurante.crear_pedido_local(5)
    assert False, "mesa ocupada deberia fallar"
except ValueError:
    pass
# mesa fuera de rango y zona invalida
try:
    restaurante.crear_pedido_local(16)
    assert False, "mesa 16 deberia fallar"
except ValueError:
    pass
try:
    restaurante.crear_pedido_delivery(r_ana, "Tiquipaya", "Calle 1")
    assert False, "zona invalida deberia fallar"
except ValueError:
    pass
# al cancelar, la mesa se libera
r_local.cancelar()
r_local_2 = restaurante.crear_pedido_local(5)
assert r_local_2.mesa == 5


# pago de mentira SOLO para probar Restaurante mientras pagos.py es el esqueleto
# (cuando se una el codigo de Anahi se cambia por PagoEfectivo, PagoQr y PagoTarjeta)
class PagoPrueba(Pago):
    def __init__(self, acepta):
        super().__init__("Prueba")
        self._acepta = acepta

    def calcular_monto(self):
        return self._monto_base

    def procesar_pago(self, total):
        self._monto_base = total
        return f"Total: Bs {total:.2f}"

    def acepta_delivery(self):
        return self._acepta


# delivery a Quillacollo con 2 combos clasicos: 82 + 15 = Bs 97
r_delivery.agregar_producto(r_combo, 2)
assert r_delivery.calcular_total() == 97.00

# no se cobra en REGISTRADO
try:
    restaurante.cobrar_pedido(r_delivery.numero, PagoPrueba(True))
    assert False, "no se cobra un pedido REGISTRADO"
except ValueError:
    pass

r_delivery.cambiar_estado(Pedido.EN_PREPARACION)
r_delivery.cambiar_estado(Pedido.LISTO)

# un pago que no acepta delivery se rechaza y el pedido sigue sin pagar
try:
    restaurante.cobrar_pedido(r_delivery.numero, PagoPrueba(False))
    assert False, "el delivery deberia rechazar este pago"
except ValueError:
    pass
assert not r_delivery.esta_pagado()

# cobro correcto en LISTO: devuelve el comprobante y marca el pedido como pagado
r_comprobante = restaurante.cobrar_pedido(r_delivery.numero, PagoPrueba(True))
assert "97.00" in r_comprobante
assert r_delivery.esta_pagado()

# no se cobra dos veces
try:
    restaurante.cobrar_pedido(r_delivery.numero, PagoPrueba(True))
    assert False, "no se cobra dos veces"
except ValueError:
    pass

# no se cobra un pedido cancelado
try:
    restaurante.cobrar_pedido(r_local.numero, PagoPrueba(True))
    assert False, "no se cobra un pedido cancelado"
except ValueError:
    pass

# tambien se cobra en ENTREGADO
r_llevar.agregar_producto(r_silpancho, 1)
r_llevar.cambiar_estado(Pedido.EN_PREPARACION)
r_llevar.cambiar_estado(Pedido.LISTO)
r_llevar.cambiar_estado(Pedido.ENTREGADO)
restaurante.cobrar_pedido(r_llevar.numero, PagoPrueba(False))
assert r_llevar.esta_pagado()

# reporte del dia por tipo: solo pagados (delivery 97 y para llevar 35 + 2 de envase = 37)
r_reporte = restaurante.reporte_ventas_dia()
assert r_reporte["Delivery"] == {"pedidos": 1, "total": 97.00}
assert r_reporte["Para llevar"] == {"pedidos": 1, "total": 37.00}
assert "Local" not in r_reporte  # el local cancelado y el abierto no se pagaron

# top de productos: un pedido sin pagar no cuenta
r_local_2.agregar_producto(r_moco, 10)
r_top = restaurante.top_productos(3)
assert len(r_top) == 2
assert r_top[0][0] is r_combo and r_top[0][1] == 2
assert r_top[1][0] is r_silpancho and r_top[1][1] == 1
assert len(restaurante.top_productos(1)) == 1


print("Todas las pruebas pasaron")
