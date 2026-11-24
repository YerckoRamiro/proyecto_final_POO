from abc import ABC, abstractmethod
from datetime import datetime
from modelo.productos import DIAS_SEMANA


class PedidoProducto:
    CANTIDAD_MIN = 1
    CANTIDAD_MAX = 20

    def __init__(self, pedido, producto, cantidad):
        self._pedido = pedido
        self._producto = producto
        self.cantidad = cantidad

    @property
    def pedido(self):
        return self._pedido

    @property
    def producto(self):
        return self._producto

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        # Bloque 1: validar entre CANTIDAD_MIN y CANTIDAD_MAX
        self._cantidad = valor

    def calcular_precio(self):
        # producto.calcular_precio() * cantidad
        pass

    def contar_platos(self):
        # producto.contar_platos() * cantidad
        pass


class Pedido(ABC):
    REGISTRADO = "REGISTRADO"
    EN_PREPARACION = "EN_PREPARACION"
    LISTO = "LISTO"
    ENTREGADO = "ENTREGADO"
    CANCELADO = "CANCELADO"

    # a que estados se puede pasar desde cada estado
    TRANSICIONES = {
        REGISTRADO: [EN_PREPARACION, CANCELADO],
        EN_PREPARACION: [LISTO],
        LISTO: [ENTREGADO],
        ENTREGADO: [],
        CANCELADO: [],
    }

    _contador = 0

    def __init__(self, cliente, dia=None):
        Pedido._contador = Pedido._contador + 1
        self._numero = Pedido._contador
        self._cliente = cliente
        self._estado = Pedido.REGISTRADO
        self._items = []
        self._fecha_hora = datetime.now()
        # el dia sale de la fecha actual, pero se puede pasar uno para probar
        if dia is None:
            dia = DIAS_SEMANA[self._fecha_hora.weekday()]
        self._dia = dia
        self._pago = None

    @property
    def numero(self):
        return self._numero

    @property
    def cliente(self):
        return self._cliente

    @property
    def estado(self):
        return self._estado

    @property
    def items(self):
        return list(self._items)

    @property
    def fecha_hora(self):
        return self._fecha_hora

    @property
    def dia(self):
        return self._dia

    @property
    def pago(self):
        return self._pago

    def agregar_producto(self, producto, cantidad):
        # solo en REGISTRADO; verifica producto.esta_disponible(self._dia); si ya existe suma cantidades
        pass

    def quitar_producto(self, producto):
        # solo en REGISTRADO
        pass

    def calcular_subtotal(self):
        pass

    def contar_platos(self):
        pass

    def calcular_total(self):
        # subtotal - descuento + cargos
        pass

    def cambiar_estado(self, nuevo):
        # revisa TRANSICIONES; al pasar a EN_PREPARACION exige items y validar_para_preparar()
        pass

    def cancelar(self):
        # solo desde REGISTRADO
        pass

    def esta_abierto(self):
        # abierto = no ENTREGADO ni CANCELADO
        pass

    def ocupa_mesa(self, mesa):
        # por defecto un pedido no ocupa mesa; PedidoLocal lo sobrescribe
        return False

    def puede_pagar_con(self, pago):
        # por defecto acepta cualquier pago; PedidoDelivery lo sobrescribe
        return True

    def marcar_pagado(self, pago):
        # guarda el pago usado
        pass

    def esta_pagado(self):
        pass

    @abstractmethod
    def calcular_cargos(self):
        pass

    @abstractmethod
    def calcular_descuento(self):
        pass

    @abstractmethod
    def obtener_tipo(self):
        pass

    @abstractmethod
    def validar_para_preparar(self):
        pass


class PedidoLocal(Pedido):
    _mesa_min = 1
    _mesa_max = 15
    # SUPUESTO: el 5 % es sobre el subtotal y cuenta los platos dentro de combos (contar_platos())
    _platos_des = 6
    _desc_grupo = 0.05

    def __init__(self, mesa, cliente=None, dia=None):
        super().__init__(cliente, dia)
        self.mesa = mesa

    @property
    def mesa_min(self):
        return self._mesa_min

    @property
    def mesa_max(self):
        return self._mesa_max

    @property
    def platos_des(self):
        return self._platos_des

    @property
    def desc_grupo(self):
        return self._desc_grupo

    @property
    def mesa(self):
        return self._mesa

    @mesa.setter
    def mesa(self, valor):
        # Bloque 1: validar entre mesa_min y mesa_max
        self._mesa = valor

    def calcular_cargos(self):
        # en el local no hay cargos
        pass

    def calcular_descuento(self):
        # desc_grupo del subtotal si contar_platos() >= platos_des
        pass

    def obtener_tipo(self):
        pass

    def validar_para_preparar(self):
        pass

    def ocupa_mesa(self, mesa):
        # misma mesa y pedido abierto
        pass


class PedidoLlevar(Pedido):
    _costo_envase = 2  # Bs por plato

    def __init__(self, cliente, dia=None):
        super().__init__(cliente, dia)

    @property
    def costo_envase(self):
        return self._costo_envase

    def calcular_cargos(self):
        # contar_platos() * costo_envase (platos dentro de combos cuentan, bebidas no)
        pass

    def calcular_descuento(self):
        pass

    def obtener_tipo(self):
        pass

    def validar_para_preparar(self):
        pass


class PedidoDelivery(Pedido):
    ZONAS = {"Cercado": 8, "Quillacollo": 15, "Sacaba": 15, "Vinto": 20}
    # SUPUESTO: el minimo se mide sobre el subtotal, sin el envio
    _pedido_minimo = 60

    def __init__(self, cliente, zona, direccion_ent, dia=None):
        super().__init__(cliente, dia)
        self.zona = zona
        self.direccion_ent = direccion_ent

    @property
    def pedido_minimo(self):
        return self._pedido_minimo

    @property
    def zona(self):
        return self._zona

    @zona.setter
    def zona(self, valor):
        # Bloque 1: validar que la zona este en ZONAS
        self._zona = valor

    @property
    def direccion_ent(self):
        return self._direccion_ent

    @direccion_ent.setter
    def direccion_ent(self, valor):
        # Bloque 1: validar que no este vacia
        self._direccion_ent = valor

    def calcular_cargos(self):
        # costo de la zona (nunca es gratis en la variante D)
        pass

    def calcular_descuento(self):
        pass

    def obtener_tipo(self):
        pass

    def validar_para_preparar(self):
        # exige subtotal >= pedido_minimo
        pass

    def puede_pagar_con(self, pago):
        # pago.acepta_delivery()
        pass
