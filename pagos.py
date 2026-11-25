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
        try:
            numero = float(valor)
        except (TypeError, ValueError):
            raise ValueError("El monto recibido debe ser un numero")
        if numero <= 0:
            raise ValueError("El monto recibido debe ser mayor a 0")
        self._monto_recibido = round(numero, 2)

    @property
    def cambio(self):
        return self._cambio

    def calcular_cambio(self):
        return round(self._monto_recibido - self._monto_base, 2)

    def calcular_monto(self):
        # el efectivo no tiene recargo
        return round(self._monto_base, 2)

    def procesar_pago(self, total):
        if total <= 0:
            raise ValueError("El total a pagar debe ser mayor a 0")
        if self._monto_recibido < total:
            raise ValueError("El monto recibido no alcanza para cubrir el total")
        self._monto_base = round(total, 2)
        self._fecha_hora = datetime.now()
        self._cambio = self.calcular_cambio()
        return (
            "Pago en efectivo\n"
            "Fecha: " + self._fecha_hora.strftime("%d/%m/%Y %H:%M") + "\n"
            "Total: Bs " + format(self.calcular_monto(), ".2f") + "\n"
            "Recibido: Bs " + format(self._monto_recibido, ".2f") + "\n"
            "Cambio: Bs " + format(self._cambio, ".2f")
        )

    def acepta_delivery(self):
        # SUPUESTO: el efectivo si se acepta en delivery (solo la tarjeta no)
        return True


class PagoQr(Pago):
    # SUPUESTO: el codigo de transaccion QR tiene exactamente 10 digitos
    LARGO_CODIGO = 10

    def __init__(self, cod_trans):
        super().__init__("QR")
        self.cod_trans = cod_trans

    @property
    def cod_trans(self):
        return self._cod_trans

    @cod_trans.setter
    def cod_trans(self, valor):
        texto = str(valor).strip()
        if len(texto) != self.LARGO_CODIGO or not texto.isdigit():
            raise ValueError(
                "El codigo de transaccion debe tener exactamente "
                + str(self.LARGO_CODIGO) + " digitos"
            )
        self._cod_trans = texto

    def calcular_monto(self):
        # el pago por QR no tiene recargo
        return round(self._monto_base, 2)

    def procesar_pago(self, total):
        if total <= 0:
            raise ValueError("El total a pagar debe ser mayor a 0")
        self._monto_base = round(total, 2)
        self._fecha_hora = datetime.now()
        return (
            "Pago por QR\n"
            "Fecha: " + self._fecha_hora.strftime("%d/%m/%Y %H:%M") + "\n"
            "Codigo de transaccion: " + self._cod_trans + "\n"
            "Total: Bs " + format(self.calcular_monto(), ".2f")
        )

    def acepta_delivery(self):
        # SUPUESTO: el QR si se acepta en delivery (solo la tarjeta no)
        return True


class PagoTarjeta(Pago):
    # SUPUESTO: la tarjeta cobra un recargo del 3% que paga el cliente
    RECARGO = 0.03

    def __init__(self):
        super().__init__("Tarjeta")

    def calcular_comision(self):
        # monto_base * RECARGO (la paga el cliente)
        return round(self._monto_base * self.RECARGO, 2)

    def calcular_monto(self):
        # monto_base + calcular_comision()
        return round(self._monto_base + self.calcular_comision(), 2)

    def procesar_pago(self, total):
        if total <= 0:
            raise ValueError("El total a pagar debe ser mayor a 0")
        self._monto_base = round(total, 2)
        self._fecha_hora = datetime.now()
        return (
            "Pago con tarjeta\n"
            "Fecha: " + self._fecha_hora.strftime("%d/%m/%Y %H:%M") + "\n"
            "Subtotal: Bs " + format(self._monto_base, ".2f") + "\n"
            "Comision: Bs " + format(self.calcular_comision(), ".2f") + "\n"
            "Total: Bs " + format(self.calcular_monto(), ".2f")
        )

    def acepta_delivery(self):
        # la tarjeta NO se acepta en delivery
        return False