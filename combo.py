from producto import Producto
class Combo(Producto):
    def __init__(self, descuento, max_producto):
        self.descuento = descuento
        self.max_producto = max_producto