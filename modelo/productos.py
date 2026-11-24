from abc import ABC, abstractmethod

# Dias sin tildes, en el orden de datetime.weekday() (0 = lunes)
DIAS_SEMANA = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]


class Producto(ABC):
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        # Bloque 1: validar que no este vacio
        self._nombre = valor

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        # Bloque 1: validar precio > 0 (es el UNICO lugar donde se valida el precio)
        self._precio = valor

    @abstractmethod
    def calcular_precio(self):
        pass

    @abstractmethod
    def esta_disponible(self, dia):
        pass

    @abstractmethod
    def contar_platos(self):
        pass

    def contiene_a(self, producto):
        # un producto simple solo se contiene a si mismo; Combo lo sobrescribe
        return self is producto


class Plato(Producto):
    def __init__(self, nombre, precio, dias_disponibles=None):
        super().__init__(nombre, precio)
        if dias_disponibles is None:
            dias_disponibles = list(DIAS_SEMANA)
        self.dias_disponibles = dias_disponibles

    @property
    def dias_disponibles(self):
        return list(self._dias_disponibles)

    @dias_disponibles.setter
    def dias_disponibles(self, valor):
        # Bloque 1: validar que cada dia este en DIAS_SEMANA
        self._dias_disponibles = list(valor)

    def calcular_precio(self):
        # precio del plato
        pass

    def esta_disponible(self, dia):
        # el dia esta en dias_disponibles
        pass

    def contar_platos(self):
        # un plato cuenta como 1
        pass


class Bebida(Producto):
    VASOS_POR_JARRA = 3

    def __init__(self, nombre, precio_vaso, tipo, categoria):
        # el precio del padre es el precio del vaso (no se repite el atributo)
        super().__init__(nombre, precio_vaso)
        self.tipo = tipo
        self.categoria = categoria

    @property
    def precio_vaso(self):
        return self.precio

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, valor):
        # Bloque 1: validar "vaso" o "jarra"
        self._tipo = valor

    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, valor):
        # Bloque 1: validar "refresco natural" o "gaseosa"
        self._categoria = valor

    def calcular_vaso(self):
        # cuantos vasos equivale: vaso = 1, jarra = VASOS_POR_JARRA
        pass

    def calcular_precio(self):
        # precio_vaso * calcular_vaso()
        pass

    def esta_disponible(self, dia):
        # las bebidas siempre estan disponibles
        pass

    def contar_platos(self):
        # una bebida no es plato
        pass


class ComboProducto:
    def __init__(self, producto, cantidad):
        self._producto = producto
        self.cantidad = cantidad

    @property
    def producto(self):
        return self._producto

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        # Bloque 1: validar cantidad >= 1
        self._cantidad = valor

    def calcular_precio(self):
        # producto.calcular_precio() * cantidad
        pass

    def contar_platos(self):
        # producto.contar_platos() * cantidad
        pass


class Combo(Producto):
    MIN_PRODUCTOS = 2
    # SUPUESTO: con 2 productos no hay descuento; "3 o mas" cuenta los productos directos (un combo interno cuenta como 1)
    MIN_PRODUCTOS_DESCUENTO = 3
    DESCUENTO = 0.15

    def __init__(self, nombre, productos):
        # Opcion 1: al padre le pasamos la suma inicial (asi valida precio > 0),
        # pero el precio real del combo se calcula en vivo en calcular_precio()
        suma = 0
        for producto in productos:
            suma = suma + producto.calcular_precio()
        super().__init__(nombre, suma)
        self._productos = []
        # Bloque 1: validar minimo MIN_PRODUCTOS y agregar cada producto con agregar_producto()

    @property
    def productos(self):
        return list(self._productos)

    def agregar_producto(self, producto, cantidad=1):
        # no puede contenerse a si mismo (usar producto.contiene_a(self))
        pass

    def quitar_producto(self, producto):
        # nunca menos de MIN_PRODUCTOS
        pass

    def calcular_precio(self):
        # suma de cada ComboProducto * (1 - DESCUENTO) si hay MIN_PRODUCTOS_DESCUENTO o mas
        pass

    def esta_disponible(self, dia):
        # disponible solo si todos sus productos lo estan
        pass

    def contar_platos(self):
        # suma de los platos de sus productos
        pass

    def contiene_a(self, producto):
        # self is producto o algun hijo lo contiene (evita ciclos)
        pass
