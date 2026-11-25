from modelo.productos import Combo, DIAS_SEMANA
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
        self._menu.append(producto)

    def armar_combo(self, nombre, productos):
        # Combo valida el minimo de productos y que no haya ciclos
        combo = Combo(nombre, productos)
        self.registrar_producto(combo)
        return combo

    def listar_menu(self, dia):
        if dia not in DIAS_SEMANA:
            raise ValueError(f"Dia invalido: {dia}")
        disponibles = []
        for producto in self._menu:
            # cada producto sabe si se vende ese dia (plato, bebida o combo)
            if producto.esta_disponible(dia):
                disponibles.append(producto)
        return disponibles

    def registrar_cliente(self, nombre, celular, correo, password, direccion):
        # el celular identifica al cliente en buscar_cliente, no puede repetirse
        for cliente in self._clientes:
            if cliente.celular == celular:
                raise ValueError(f"Ya existe un cliente con el celular {celular}")
        # Cliente valida sus propios datos en sus setters
        cliente = Cliente(nombre, celular, correo, password, direccion)
        self._clientes.append(cliente)
        return cliente

    def buscar_cliente(self, celular):
        for cliente in self._clientes:
            if cliente.celular == celular:
                return cliente
        raise ValueError(f"No existe un cliente con el celular {celular}")

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
