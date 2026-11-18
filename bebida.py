from producto import Producto
class Bebida(Producto):
    def __init__(self, tipo, precio_vaso):
        self.tipo = tipo 
        self.precio_vaso = precio_vaso
    def calcular_vaso(self):
        pass
    