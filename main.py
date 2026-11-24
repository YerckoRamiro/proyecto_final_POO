from restaurante import Restaurante
from modelo.productos import Plato, Bebida
from modelo.pagos import PagoEfectivo, PagoQr, PagoTarjeta


def cargar_datos_ejemplo(restaurante):
    # Bloque 2: silpancho, pique macho, chicharron (domingo), sopa de mani, mocochinchi, gaseosa
    pass


def main():
    restaurante = Restaurante()
    cargar_datos_ejemplo(restaurante)
    # Bloque 2: menu numerado con while y try/except ValueError


main()
