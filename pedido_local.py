from pedido import Pedido
class PedidoLocal(Pedido):
    def __init__ (self, mesa_min, mesa_max, platos_des, desc_grupo):
        self.mesa_min = mesa_min
        self.mesa_max = mesa_max
        self.platos_desc = platos_des
        self.desc_grupo = desc_grupo
    
        