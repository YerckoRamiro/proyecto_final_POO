class Cliente:
    def __init__(self, nombre, celular, correo, password, direccion):
        self.nombre = nombre
        self.celular = celular
        self.correo = correo
        # privado: solo esta clase lo toca, no tiene property de lectura
        self.__password = password
        self.direccion = direccion

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

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        # Bloque 1: validar que no este vacio
        self.__correo = valor

    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, valor):
        # Bloque 1: validar que no este vacia
        self._direccion = valor

    def verificar_password(self, texto):
        # compara sin mostrar nunca el password
        pass
