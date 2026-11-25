from datetime import datetime
from modelo.productos import Combo, DIAS_SEMANA
from modelo.pedidos import Pedido, PedidoLocal, PedidoLlevar, PedidoDelivery
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
        # cada pedido responde si ocupa la mesa: para llevar y delivery dicen False (sin isinstance)
        for pedido in self._pedidos:
            if pedido.ocupa_mesa(mesa):
                raise ValueError(f"La mesa {mesa} ya tiene un pedido abierto")
        pedido = PedidoLocal(mesa)
        self._pedidos.append(pedido)
        return pedido

    def crear_pedido_para_llevar(self, cliente):
        pedido = PedidoLlevar(cliente)
        self._pedidos.append(pedido)
        return pedido

    def crear_pedido_delivery(self, cliente, zona, direccion_ent):
        # PedidoDelivery valida la zona y la direccion
        pedido = PedidoDelivery(cliente, zona, direccion_ent)
        self._pedidos.append(pedido)
        return pedido

    def buscar_pedido(self, numero):
        for pedido in self._pedidos:
            if pedido.numero == numero:
                return pedido
        raise ValueError(f"No existe el pedido numero {numero}")

    def cobrar_pedido(self, numero, pago):
        pedido = self.buscar_pedido(numero)
        # confirmado: se cobra en LISTO o ENTREGADO (asi un CANCELADO nunca se cobra)
        if pedido.estado != Pedido.LISTO and pedido.estado != Pedido.ENTREGADO:
            raise ValueError(f"Solo se cobra un pedido LISTO o ENTREGADO (esta {pedido.estado})")
        if pedido.esta_pagado():
            raise ValueError(f"El pedido {numero} ya fue pagado")
        # cada pedido decide que pagos acepta (delivery: solo efectivo o QR)
        if not pedido.puede_pagar_con(pago):
            raise ValueError(f"El pedido {pedido.obtener_tipo()} no acepta pago con {pago.nombre}")
        # primero se procesa: si el pago falla, el pedido no queda pagado
        comprobante = pago.procesar_pago(pedido.calcular_total())
        pedido.marcar_pagado(pago)
        return f"Pedido N. {numero} ({pedido.obtener_tipo()})\n{comprobante}"

    def reporte_ventas_dia(self):
        # {"Local": {"pedidos": 2, "total": 120.5}, ...} solo con pedidos pagados de hoy
        hoy = datetime.now().date()
        reporte = {}
        for pedido in self._pedidos:
            if pedido.esta_pagado() and pedido.fecha_hora.date() == hoy:
                # la clave la da cada pedido con obtener_tipo() (sin isinstance)
                tipo = pedido.obtener_tipo()
                if tipo not in reporte:
                    reporte[tipo] = {"pedidos": 0, "total": 0}
                reporte[tipo]["pedidos"] = reporte[tipo]["pedidos"] + 1
                reporte[tipo]["total"] = round(reporte[tipo]["total"] + pedido.calcular_total(), 2)
        return reporte

    def top_productos(self, cantidad):
        # cuenta las unidades vendidas de cada producto en los pedidos pagados: [[producto, unidades], ...]
        conteo = []
        for pedido in self._pedidos:
            if pedido.esta_pagado():
                for item in pedido.items:
                    encontrado = False
                    for par in conteo:
                        if par[0] is item.producto:
                            par[1] = par[1] + item.cantidad
                            encontrado = True
                    if not encontrado:
                        conteo.append([item.producto, item.cantidad])
        # elige el mas vendido, lo saca de la lista y repite
        top = []
        while len(top) < cantidad and len(conteo) > 0:
            mayor = conteo[0]
            for par in conteo:
                if par[1] > mayor[1]:
                    mayor = par
            top.append(mayor)
            conteo.remove(mayor)
        return top
