from abc import ABC, abstractmethod
from datetime import datetime


class Pago(ABC):
    def __init__(self, nombre):
        self._nombre = nombre
        # monto_base y fecha_hora se llenan al procesar el pago
        self._monto_base = 0
        self._fecha_hora = None

    @property
    def nombre(self):
        return self._nombre

    @property
    def monto_base(self):
        return self._monto_base

    @property
    def fecha_hora(self):
        return self._fecha_hora

    @abstractmethod
    def calcular_monto(self):
        pass

    @abstractmethod
    def procesar_pago(self, total):
        # guarda monto_base y fecha_hora (datetime.now()), valida y devuelve el texto del comprobante
        pass

    @abstractmethod
    def acepta_delivery(self):
        pass


class PagoEfectivo(Pago):
    def __init__(self, monto_recibido):
        super().__init__("Efectivo")
        self.monto_recibido = monto_recibido
        self._cambio = 0

    @property
    def monto_recibido(self):
        return self._monto_recibido

    @monto_recibido.setter
    def monto_recibido(self, valor):
        # Bloque 1: validar monto > 0
        self._monto_recibido = valor

    @property
    def cambio(self):
        return self._cambio

    def calcular_cambio(self):
        # monto_recibido - monto_base
        pass

    def calcular_monto(self):
        # el efectivo no tiene recargo
        pass

    def procesar_pago(self, total):
        # exige monto_recibido >= total y calcula el cambio
        pass

    def acepta_delivery(self):
        pass


class PagoQr(Pago):
    LARGO_CODIGO = 10

    def __init__(self, cod_trans):
        super().__init__("QR")
        self.cod_trans = cod_trans

    @property
    def cod_trans(self):
        return self._cod_trans

    @cod_trans.setter
    def cod_trans(self, valor):
        # Bloque 1: validar exactamente LARGO_CODIGO digitos
        self._cod_trans = valor

    def calcular_monto(self):
        pass

    def procesar_pago(self, total):
        pass

    def acepta_delivery(self):
        pass


class PagoTarjeta(Pago):
    _recargo = 0.03  # comision del 3 % a cargo del cliente

    def __init__(self):
        super().__init__("Tarjeta")

    @property
    def recargo(self):
        return self._recargo

    def calcular_comision(self):
        # monto_base * recargo
        pass

    def calcular_monto(self):
        # monto_base + calcular_comision()
        pass

    def procesar_pago(self, total):
        pass

    def acepta_delivery(self):
        # la tarjeta NO se acepta en delivery
        pass
