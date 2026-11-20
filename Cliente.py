class Cliente:
    def __init__(self, nombre, correo, password, celular, direcciones):
        self.nombre = nombre
        self.__correo = correo
        self.__password = password
        self.celular = celular
        self.direcciones = direcciones

    def Obtner_correo(self):
        return self.__correo
    
    def Obtener_password(self):
        return self.__password