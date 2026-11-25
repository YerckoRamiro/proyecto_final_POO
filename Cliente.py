class Cliente:
    def __init__(self, nombre, celular, correo, password, direccion):
        self.nombre = nombre
        self.celular = celular
        self.correo = correo
        # la contrasena es privada y no tiene property de lectura
        if password is None or str(password).strip() == "":
            raise ValueError("La contrasena no puede estar vacia")
        self.__password = str(password)
        self.direccion = direccion

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

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ValueError("El correo no puede estar vacio")
        self.__correo = str(valor).strip()

    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ValueError("La direccion no puede estar vacia")
        self._direccion = str(valor).strip()

    def verificar_password(self, texto):
        return self.__password == texto