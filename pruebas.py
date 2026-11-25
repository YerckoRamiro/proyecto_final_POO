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

# Datos de prueba propios con prefijo p_
p_silpancho = Plato("Silpancho", 35)
p_moco = Bebida("Mocochinchi", 6, "vaso", "refresco natural")
p_combo = Combo("Combo clasico", [p_silpancho, p_moco])
p_cliente = Cliente("Ana", "71234567", "ana@correo.com", "clave", "Calle 1")

# 1. Local con 6 silpanchos: subtotal 210, descuento 10.5, total 199.50
p_local_6 = PedidoLocal(1, dia="martes")
p_local_6.agregar_producto(p_silpancho, 6)
assert p_local_6.calcular_subtotal() == 210.00
assert p_local_6.calcular_descuento() == 10.50
assert p_local_6.calcular_total() == 199.50

# 2. Local con 5 silpanchos: descuento 0 (no llega a 6 platos)
p_local_5 = PedidoLocal(2, dia="martes")
p_local_5.agregar_producto(p_silpancho, 5)
assert p_local_5.calcular_descuento() == 0

# 3. Para llevar con 3 combos + 2 mocochinchi: cargos 6 (platos del combo cuentan, bebidas no)
p_llevar = PedidoLlevar(p_cliente, dia="martes")
p_llevar.agregar_producto(p_combo, 3)
p_llevar.agregar_producto(p_moco, 2)
assert p_llevar.calcular_cargos() == 6.00

# 4. Delivery a Quillacollo con 2 combos: subtotal 82, cargos 15, total 97 (sin envio gratis)
p_delivery = PedidoDelivery(p_cliente, "Quillacollo", "Av. Blanco Galindo", dia="martes")
p_delivery.agregar_producto(p_combo, 2)
assert p_delivery.calcular_subtotal() == 82.00
assert p_delivery.calcular_cargos() == 15.00
assert p_delivery.calcular_total() == 97.00

# 5. Delivery a Cercado con 1 silpancho (35) -> cambiar_estado(EN_PREPARACION) falla (minimo Bs 60)
p_del_min = PedidoDelivery(p_cliente, "Cercado", "Calle Sucre 10", dia="martes")
p_del_min.agregar_producto(p_silpancho, 1)
try:
    p_del_min.cambiar_estado(Pedido.EN_PREPARACION)
    assert False, "delivery bajo Bs 60 deberia fallar"
except ValueError:
    pass

# 6. Pedido nuevo -> cambiar_estado(Pedido.LISTO) falla (transicion invalida)
p_estado = PedidoLocal(3, dia="martes")
p_estado.agregar_producto(p_silpancho, 1)
try:
    p_estado.cambiar_estado(Pedido.LISTO)
    assert False, "transicion de REGISTRADO a LISTO deberia fallar"
except ValueError:
    pass

# 7. Pedido en EN_PREPARACION -> cancelar() falla
p_estado.cambiar_estado(Pedido.EN_PREPARACION)
try:
    p_estado.cancelar()
    assert False, "cancelar en EN_PREPARACION deberia fallar"
except ValueError:
    pass

# 8. Pedido en EN_PREPARACION -> agregar_producto(...) y quitar_producto(...) fallan
try:
    p_estado.agregar_producto(p_moco, 1)
    assert False, "agregar producto en EN_PREPARACION deberia fallar"
except ValueError:
    pass
try:
    p_estado.quitar_producto(p_silpancho)
    assert False, "quitar producto en EN_PREPARACION deberia fallar"
except ValueError:
    pass

# 9. PedidoLocal(0) y PedidoLocal(16) fallan
try:
    PedidoLocal(0, dia="martes")
    assert False, "mesa 0 deberia fallar"
except ValueError:
    pass
try:
    PedidoLocal(16, dia="martes")
    assert False, "mesa 16 deberia fallar"
except ValueError:
    pass

# 10. agregar_producto con cantidad 0 y 21 fallan
p_val = PedidoLocal(4, dia="martes")
try:
    p_val.agregar_producto(p_silpancho, 0)
    assert False, "cantidad 0 deberia fallar"
except ValueError:
    pass
try:
    p_val.agregar_producto(p_silpancho, 21)
    assert False, "cantidad 21 deberia fallar"
except ValueError:
    pass

# 11. 20 silpanchos y luego 1 mas falla, y la cantidad sigue en 20
p_val.agregar_producto(p_silpancho, 20)
try:
    p_val.agregar_producto(p_silpancho, 1)
    assert False, "sumar mas de 20 unidades deberia fallar"
except ValueError:
    pass
assert p_val.items[0].cantidad == 20

# 12. Encapsulacion: pedido.items[0].cantidad = 20 lanza AttributeError
try:
    p_val.items[0].cantidad = 20
    assert False, "modificar cantidad desde fuera deberia lanzar AttributeError"
except AttributeError:
    pass

# 13. PedidoLocal(3, dia="Domingo") falla (dia mal escrito)
try:
    PedidoLocal(3, dia="Domingo")
    assert False, "dia mal escrito deberia fallar"
except ValueError:
    pass

# 14. PedidoLlevar(None) y PedidoDelivery(None, ...) fallan (exigen cliente)
try:
    PedidoLlevar(None, dia="martes")
    assert False, "para llevar sin cliente deberia fallar"
except ValueError:
    pass
try:
    PedidoDelivery(None, "Cercado", "Calle 1", dia="martes")
    assert False, "delivery sin cliente deberia fallar"
except ValueError:
    pass

# 15. marcar_pagado(...) en un pedido REGISTRADO falla
# (Descomentar cuando Anahi una PagoQr a main; pagos.py aun es el esqueleto)
# p_sin_pagar = PedidoLocal(5, dia="martes")
# p_sin_pagar.agregar_producto(p_silpancho, 1)
# try:
#     p_sin_pagar.marcar_pagado(PagoQr("1234567890"))
#     assert False, "marcar_pagado en REGISTRADO deberia fallar"
# except ValueError:
#     pass

# ===== PRUEBAS DE PAGOS Y CLIENTES ===== (Anahi)

# Pago es abstracta
try:
    Pago("prueba")
    assert False, "Pago no deberia poder instanciarse"
except TypeError:
    pass

# PagoEfectivo calcula el cambio
pago = PagoEfectivo(50)
pago.procesar_pago(41)
assert pago.cambio == 9.0

# PagoEfectivo exacto (cambio 0)
pago_exacto = PagoEfectivo(41)
pago_exacto.procesar_pago(41)
assert pago_exacto.cambio == 0

# PagoEfectivo rechaza un monto que no alcanza
try:
    PagoEfectivo(10).procesar_pago(41)
    assert False, "PagoEfectivo deberia rechazar un monto insuficiente"
except ValueError:
    pass

# PagoEfectivo rechaza un monto recibido de 0
try:
    PagoEfectivo(0)
    assert False, "PagoEfectivo deberia rechazar un monto de 0"
except ValueError:
    pass

# PagoQr acepta un codigo de 10 digitos
pago = PagoQr("1234567890")
assert pago.cod_trans == "1234567890"

# PagoQr rechaza un codigo corto
try:
    PagoQr("123")
    assert False, "PagoQr deberia rechazar un codigo de largo incorrecto"
except ValueError:
    pass

# PagoQr rechaza un codigo de 11 digitos
try:
    PagoQr("12345678901")
    assert False, "PagoQr deberia rechazar un codigo de 11 digitos"
except ValueError:
    pass

# PagoQr rechaza un codigo con letras
try:
    PagoQr("12345abcde")
    assert False, "PagoQr deberia rechazar un codigo con letras"
except ValueError:
    pass

# PagoTarjeta cobra 3% de recargo
pago = PagoTarjeta()
pago.procesar_pago(41)
assert pago.recargo == 0.03
assert pago.calcular_comision() == 1.23
assert pago.calcular_monto() == 42.23

# PagoTarjeta con decimales (88.80)
pago_tarjeta_dec = PagoTarjeta()
pago_tarjeta_dec.procesar_pago(88.80)
assert pago_tarjeta_dec.calcular_comision() == 2.66
assert pago_tarjeta_dec.calcular_monto() == 91.46

# La tarjeta no se acepta en delivery, el efectivo y el QR si
assert PagoTarjeta().acepta_delivery() is False
assert PagoEfectivo(50).acepta_delivery() is True
assert PagoQr("1234567890").acepta_delivery() is True

# Cliente valido
cliente = Cliente("Ana", "71234567", "ana@correo.com", "clave123", "Calle Sucre 10")
assert cliente.nombre == "Ana"
assert cliente.celular == "71234567"
assert cliente.correo == "ana@correo.com"
assert cliente.direccion == "Calle Sucre 10"

# Tarjeta rechazada en PedidoDelivery y QR aceptado
pedido_del = PedidoDelivery(cliente, "Cercado", "Calle 1")
assert pedido_del.puede_pagar_con(PagoTarjeta()) is False
assert pedido_del.puede_pagar_con(PagoQr("1234567890")) is True

# La contrasena se verifica pero no se puede leer
assert cliente.verificar_password("clave123") is True
assert cliente.verificar_password("otra") is False
assert not hasattr(cliente, "password")

# Cliente rechaza nombre vacio
try:
    Cliente("", "71234567", "ana@correo.com", "clave123", "Calle Sucre 10")
    assert False, "Cliente deberia rechazar un nombre vacio"
except ValueError:
    pass

# Cliente rechaza celular que no empieza en 6 o 7
try:
    Cliente("Ana", "51234567", "ana@correo.com", "clave123", "Calle Sucre 10")
    assert False, "Cliente deberia rechazar un celular que empieza en 5"
except ValueError:
    pass

# Cliente rechaza celular de largo incorrecto
try:
    Cliente("Ana", "7123", "ana@correo.com", "clave123", "Calle Sucre 10")
    assert False, "Cliente deberia rechazar un celular corto"
except ValueError:
    pass

# Cliente rechaza celular con letras
try:
    Cliente("Ana", "7123456a", "ana@correo.com", "clave123", "Calle Sucre 10")
    assert False, "Cliente deberia rechazar un celular con letras"
except ValueError:
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
# un celular invalido tambien se rechaza al registrar el cliente
try:
    restaurante.registrar_cliente("Beto", "51234567", "beto@correo.com", "x", "Calle 3")
    assert False, "celular que empieza en 5 deberia fallar"
except ValueError:
    pass
# SUPUESTO: para llevar y delivery necesitan cliente
try:
    restaurante.crear_pedido_para_llevar(None)
    assert False, "para llevar sin cliente deberia fallar"
except ValueError:
    pass
try:
    restaurante.crear_pedido_delivery(None, "Cercado", "Calle 1")
    assert False, "delivery sin cliente deberia fallar"
except ValueError:
    pass
# al cancelar, la mesa se libera
r_local.cancelar()
r_local_2 = restaurante.crear_pedido_local(5)
assert r_local_2.mesa == 5


# delivery a Quillacollo con 2 combos clasicos: 82 + 15 = Bs 97
r_delivery.agregar_producto(r_combo, 2)
assert r_delivery.calcular_total() == 97.00

# no se cobra en REGISTRADO
try:
    restaurante.cobrar_pedido(r_delivery.numero, PagoQr("1234567890"))
    assert False, "no se cobra un pedido REGISTRADO"
except ValueError:
    pass

r_delivery.cambiar_estado(Pedido.EN_PREPARACION)
r_delivery.cambiar_estado(Pedido.LISTO)

# la tarjeta no se acepta en delivery y el pedido sigue sin pagar
try:
    restaurante.cobrar_pedido(r_delivery.numero, PagoTarjeta())
    assert False, "el delivery deberia rechazar la tarjeta"
except ValueError:
    pass
assert not r_delivery.esta_pagado()

# efectivo insuficiente: falla y el pedido sigue sin pagar
try:
    restaurante.cobrar_pedido(r_delivery.numero, PagoEfectivo(50))
    assert False, "el efectivo no alcanza para Bs 97"
except ValueError:
    pass
assert not r_delivery.esta_pagado()

# cobro correcto en LISTO con QR: devuelve el comprobante y marca el pedido como pagado
r_comprobante = restaurante.cobrar_pedido(r_delivery.numero, PagoQr("1234567890"))
assert "97.00" in r_comprobante
assert "1234567890" in r_comprobante
assert r_delivery.esta_pagado()

# no se cobra dos veces
try:
    restaurante.cobrar_pedido(r_delivery.numero, PagoQr("1234567890"))
    assert False, "no se cobra dos veces"
except ValueError:
    pass

# no se cobra un pedido cancelado
try:
    restaurante.cobrar_pedido(r_local.numero, PagoQr("1234567890"))
    assert False, "no se cobra un pedido cancelado"
except ValueError:
    pass

# tambien se cobra en ENTREGADO, aqui con tarjeta (37 + 3 % = 38.11)
r_llevar.agregar_producto(r_silpancho, 1)
r_llevar.cambiar_estado(Pedido.EN_PREPARACION)
r_llevar.cambiar_estado(Pedido.LISTO)
r_llevar.cambiar_estado(Pedido.ENTREGADO)
r_comprobante_tarjeta = restaurante.cobrar_pedido(r_llevar.numero, PagoTarjeta())
assert "38.11" in r_comprobante_tarjeta
assert r_llevar.esta_pagado()

# reporte del dia por tipo, solo pagados y con lo cobrado (SUPUESTO: incluye la comision)
# delivery 97; para llevar (35 + 2 de envase) * 1.03 = 38.11
r_reporte = restaurante.reporte_ventas_dia()
assert r_reporte["Delivery"] == {"pedidos": 1, "total": 97.00}
assert r_reporte["Para llevar"] == {"pedidos": 1, "total": 38.11}
assert "Local" not in r_reporte  # el local cancelado y el abierto no se pagaron

# top de productos: un pedido sin pagar no cuenta
r_local_2.agregar_producto(r_moco, 10)
r_top = restaurante.top_productos(3)
assert len(r_top) == 2
assert r_top[0][0] is r_combo and r_top[0][1] == 2
assert r_top[1][0] is r_silpancho and r_top[1][1] == 1
assert len(restaurante.top_productos(1)) == 1


print("Todas las pruebas pasaron")
