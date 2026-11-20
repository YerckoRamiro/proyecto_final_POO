from pedido import Pedido
class PedidoDelyvery(Pedido):
    def __init__(self, cliente, estado, pago, pedido_min, direccion_ent):
        self.cliente = cliente
        self.estado = estado
        self.pago = pago 
        self.pedido_min = pedido_min
        self.direccion = direccion_ent
        