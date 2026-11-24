class Cliente:
    def __init__(self, nombre, celular):
        self.nombre = nombre
        self.celular = celular

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        # Bloque 1: validar que no este vacio
        self._nombre = valor

    @property
    def celular(self):
        return self._celular

    @celular.setter
    def celular(self, valor):
        # Bloque 1: validar 8 digitos que empiezan en 6 o 7
        self._celular = valor
