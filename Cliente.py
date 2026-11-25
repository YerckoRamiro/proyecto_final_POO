class Cliente:
    def __init__(self, nombre, celular):
        self.nombre = nombre
        self.celular = celular

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ValueError("El nombre no puede estar vacio")
        self._nombre = str(valor).strip()

    @property
    def celular(self):
        return self._celular

    @celular.setter
    def celular(self, valor):
        texto = str(valor).strip()
        if len(texto) != 8 or not texto.isdigit():
            raise ValueError("El celular debe tener exactamente 8 digitos")
        if texto[0] != "6" and texto[0] != "7":
            raise ValueError("El celular debe empezar con 6 o 7")
        self._celular = texto