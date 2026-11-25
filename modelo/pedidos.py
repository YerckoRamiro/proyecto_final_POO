from abc import ABC, abstractmethod
from datetime import datetime
from modelo.productos import DIAS_SEMANA


class PedidoProducto:
    CANTIDAD_MIN = 1
    CANTIDAD_MAX = 20

    def __init__(self, pedido, producto, cantidad):
        if cantidad < self.CANTIDAD_MIN or cantidad > self.CANTIDAD_MAX:
            raise ValueError(
                f"La cantidad debe estar entre {self.CANTIDAD_MIN} y {self.CANTIDAD_MAX}."
            )
        self._pedido = pedido
        self._producto = producto
        self._cantidad = cantidad

    @property
    def pedido(self):
        return self._pedido

    @property
    def producto(self):
        return self._producto

    @property
    def cantidad(self):
        return self._cantidad

    def calcular_precio(self):
        return round(self._producto.calcular_precio() * self._cantidad, 2)

    def contar_platos(self):
        return self._producto.contar_platos() * self._cantidad


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
        fecha_actual = datetime.now()
        # el dia sale de la fecha actual, pero se puede pasar uno para probar
        if dia is None:
            dia = DIAS_SEMANA[fecha_actual.weekday()]
        if dia not in DIAS_SEMANA:
            raise ValueError(f"El dia '{dia}' no es valido.")
        Pedido._contador = Pedido._contador + 1
        self._numero = Pedido._contador
        self._cliente = cliente
        self._estado = Pedido.REGISTRADO
        self._items = []
        self._fecha_hora = fecha_actual
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
        if self._estado != Pedido.REGISTRADO:
            raise ValueError("Solo se pueden agregar productos cuando el pedido esta REGISTRADO.")
        if not producto.esta_disponible(self._dia):
            raise ValueError(f"El producto no esta disponible el dia {self._dia}.")
        if cantidad < PedidoProducto.CANTIDAD_MIN:
            raise ValueError(
                f"La cantidad debe ser al menos {PedidoProducto.CANTIDAD_MIN}."
            )
        for i in range(len(self._items)):
            if self._items[i].producto is producto:
                nueva_cantidad = self._items[i].cantidad + cantidad
                self._items[i] = PedidoProducto(self, producto, nueva_cantidad)
                return
        nuevo_item = PedidoProducto(self, producto, cantidad)
        self._items.append(nuevo_item)

    def quitar_producto(self, producto):
        if self._estado != Pedido.REGISTRADO:
            raise ValueError("Solo se pueden quitar productos cuando el pedido esta REGISTRADO.")
        for item in self._items:
            if item.producto is producto:
                self._items.remove(item)
                return
        raise ValueError("El producto no se encuentra en el pedido.")

    def calcular_subtotal(self):
        total = 0
        for item in self._items:
            total = total + item.calcular_precio()
        return round(total, 2)

    def contar_platos(self):
        total = 0
        for item in self._items:
            total = total + item.contar_platos()
        return total

    def calcular_total(self):
        total = self.calcular_subtotal() - self.calcular_descuento() + self.calcular_cargos()
        return round(total, 2)

    def cambiar_estado(self, nuevo):
        permitidos = Pedido.TRANSICIONES[self._estado]
        if nuevo not in permitidos:
            raise ValueError(f"No se puede cambiar de {self._estado} a {nuevo}.")
        if nuevo == Pedido.EN_PREPARACION:
            if len(self._items) == 0:
                raise ValueError("El pedido debe tener al menos un producto para pasar a preparacion.")
            self.validar_para_preparar()
        self._estado = nuevo

    def cancelar(self):
        self.cambiar_estado(Pedido.CANCELADO)

    def esta_abierto(self):
        return self._estado != Pedido.ENTREGADO and self._estado != Pedido.CANCELADO

    def ocupa_mesa(self, mesa):
        # por defecto un pedido no ocupa mesa; PedidoLocal lo sobrescribe
        return False

    def puede_pagar_con(self, pago):
        # por defecto acepta cualquier pago; PedidoDelivery lo sobrescribe
        return True

    def marcar_pagado(self, pago):
        if self.esta_pagado():
            raise ValueError("El pedido ya fue pagado.")
        if self._estado != Pedido.LISTO and self._estado != Pedido.ENTREGADO:
            raise ValueError("Solo se puede pagar un pedido cuando esta LISTO o ENTREGADO.")
        if not self.puede_pagar_con(pago):
            raise ValueError("Este pedido no acepta el metodo de pago elegido.")
        self._pago = pago

    def esta_pagado(self):
        return self._pago is not None

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
        if valor < self._mesa_min or valor > self._mesa_max:
            raise ValueError(
                f"La mesa debe estar entre {self._mesa_min} y {self._mesa_max}."
            )
        self._mesa = valor

    def calcular_cargos(self):
        # en el local no hay cargos
        return 0

    def calcular_descuento(self):
        # desc_grupo del subtotal si contar_platos() >= platos_des
        if self.contar_platos() >= self._platos_des:
            return round(self.calcular_subtotal() * self._desc_grupo, 2)
        return 0

    def obtener_tipo(self):
        return "Local"

    def validar_para_preparar(self):
        # no requiere validaciones adicionales
        pass

    def ocupa_mesa(self, mesa):
        # misma mesa y pedido abierto
        return self._mesa == mesa and self.esta_abierto()


class PedidoLlevar(Pedido):
    _costo_envase = 2  # Bs por plato

    def __init__(self, cliente, dia=None):
        super().__init__(cliente, dia)

    @property
    def costo_envase(self):
        return self._costo_envase

    def calcular_cargos(self):
        # contar_platos() * costo_envase (platos dentro de combos cuentan, bebidas no)
        return round(self.contar_platos() * self._costo_envase, 2)

    def calcular_descuento(self):
        return 0

    def obtener_tipo(self):
        return "Para llevar"

    def validar_para_preparar(self):
        # no requiere validaciones adicionales
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
        if valor not in self.ZONAS:
            raise ValueError("La zona de delivery no es valida.")
        self._zona = valor

    @property
    def direccion_ent(self):
        return self._direccion_ent

    @direccion_ent.setter
    def direccion_ent(self, valor):
        if valor is None or valor.strip() == "":
            raise ValueError("La direccion de entrega no puede estar vacia.")
        self._direccion_ent = valor

    def calcular_cargos(self):
        # costo de la zona (nunca es gratis en la variante D)
        return round(self.ZONAS[self._zona], 2)

    def calcular_descuento(self):
        return 0

    def obtener_tipo(self):
        return "Delivery"

    def validar_para_preparar(self):
        # exige subtotal >= pedido_minimo
        if self.calcular_subtotal() < self._pedido_minimo:
            raise ValueError(
                f"El pedido minimo para delivery es de Bs {self._pedido_minimo}."
            )

    def puede_pagar_con(self, pago):
        # pago.acepta_delivery()
        return pago.acepta_delivery()