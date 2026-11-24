from modelo.productos import Plato, Bebida, Combo
from modelo.pedidos import PedidoLocal, PedidoLlevar, PedidoDelivery
from modelo.clientes import Cliente


class Restaurante:
    def __init__(self):
        self._menu = []
        self._clientes = []
        self._pedidos = []

    @property
    def menu(self):
        return list(self._menu)

    @property
    def clientes(self):
        return list(self._clientes)

    @property
    def pedidos(self):
        return list(self._pedidos)

    def registrar_producto(self, producto):
        pass

    def armar_combo(self, nombre, productos):
        pass

    def listar_menu(self, dia):
        # solo los productos con esta_disponible(dia)
        pass

    def registrar_cliente(self, nombre, celular, correo, password, direccion):
        pass

    def buscar_cliente(self, celular):
        pass

    def crear_pedido_local(self, mesa):
        # recorre los pedidos con ocupa_mesa(mesa), sin isinstance
        pass

    def crear_pedido_para_llevar(self, cliente):
        pass

    def crear_pedido_delivery(self, cliente, zona, direccion_ent):
        pass

    def buscar_pedido(self, numero):
        pass

    def cobrar_pedido(self, numero, pago):
        # LISTO o ENTREGADO, no pagado y puede_pagar_con(pago)
        pass

    def reporte_ventas_dia(self):
        # agrupa por obtener_tipo(); solo pedidos pagados
        pass

    def top_productos(self, cantidad):
        # solo pedidos pagados
        pass
