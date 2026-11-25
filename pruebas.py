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

# PagoEfectivo calcula el cambio
pago = PagoEfectivo(50)
pago.procesar_pago(41)
assert pago.cambio == 9.0

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

# PagoTarjeta cobra 3% de recargo
pago = PagoTarjeta()
pago.procesar_pago(41)
assert pago.calcular_comision() == 1.23
assert pago.calcular_monto() == 42.23

# La tarjeta no se acepta en delivery, el efectivo y el QR si
assert PagoTarjeta().acepta_delivery() is False
assert PagoEfectivo(50).acepta_delivery() is True
assert PagoQr("1234567890").acepta_delivery() is True

# Cliente valido
cliente = Cliente("Ana", "71234567")
assert cliente.nombre == "Ana"
assert cliente.celular == "71234567"

# Cliente rechaza nombre vacio
try:
    Cliente("", "71234567")
    assert False, "Cliente deberia rechazar un nombre vacio"
except ValueError:
    pass

# Cliente rechaza celular que no empieza en 6 o 7
try:
    Cliente("Ana", "51234567")
    assert False, "Cliente deberia rechazar un celular que empieza en 5"
except ValueError:
    pass

# Cliente rechaza celular de largo incorrecto
try:
    Cliente("Ana", "7123")
    assert False, "Cliente deberia rechazar un celular corto"
except ValueError:
    pass


# ===== PRUEBAS DE RESTAURANTE ===== (integracion)


print("Todas las pruebas pasaron")