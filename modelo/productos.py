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
        if valor.strip() == "":
            raise ValueError("El nombre del producto no puede estar vacio")
        self._nombre = valor.strip()

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        # es el UNICO lugar donde se valida el precio (sirve para Plato, Bebida y Combo)
        if valor <= 0:
            raise ValueError("El precio debe ser mayor a 0")
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
        if len(valor) == 0:
            raise ValueError("El plato debe venderse al menos un dia")
        for dia in valor:
            if dia not in DIAS_SEMANA:
                raise ValueError(f"Dia invalido: {dia}. Use: {', '.join(DIAS_SEMANA)}")
        # guardamos una copia para que nadie cambie la lista desde fuera
        self._dias_disponibles = list(valor)

    def calcular_precio(self):
        return round(self.precio, 2)

    def esta_disponible(self, dia):
        return dia in self._dias_disponibles

    def contar_platos(self):
        return 1


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
        if valor != "vaso" and valor != "jarra":
            raise ValueError("El tipo de bebida debe ser 'vaso' o 'jarra'")
        self._tipo = valor

    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, valor):
        if valor != "refresco natural" and valor != "gaseosa":
            raise ValueError("La categoria debe ser 'refresco natural' o 'gaseosa'")
        self._categoria = valor

    def calcular_vaso(self):
        # cuantos vasos equivale: la jarra cuesta como 3 vasos
        if self._tipo == "jarra":
            return self.VASOS_POR_JARRA
        return 1

    def calcular_precio(self):
        return round(self.precio_vaso * self.calcular_vaso(), 2)

    def esta_disponible(self, dia):
        # las bebidas se venden todos los dias
        return True

    def contar_platos(self):
        # una bebida no es plato (no paga envase)
        return 0


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
        if valor < 1:
            raise ValueError("La cantidad en el combo debe ser al menos 1")
        self._cantidad = valor

    def calcular_precio(self):
        # no importa si el producto es plato, bebida u otro combo: cada uno sabe su precio
        return round(self._producto.calcular_precio() * self._cantidad, 2)

    def contar_platos(self):
        return self._producto.contar_platos() * self._cantidad


class Combo(Producto):
    MIN_PRODUCTOS = 2
    # SUPUESTO: con 2 productos no hay descuento; "3 o mas" cuenta las unidades directas del combo
    # (2 silpanchos + 1 mocochinchi = 3; un combo interno cuenta como 1 por unidad)
    _min_producto = 3  # productos necesarios para el descuento
    _descuento = 0.15

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
    def descuento(self):
        return self._descuento

    @property
    def min_producto(self):
        return self._min_producto

    @property
    def productos(self):
        return list(self._productos)

    def agregar_producto(self, producto, cantidad=1):
        # no puede contenerse a si mismo (usar producto.contiene_a(self))
        pass

    def quitar_producto(self, producto):
        # nunca menos de MIN_PRODUCTOS
        pass

    def contar_productos(self):
        # suma la cantidad de cada ComboProducto (se usa para MIN_PRODUCTOS y min_producto)
        pass

    def calcular_precio(self):
        # suma de cada ComboProducto * (1 - descuento) si contar_productos() >= min_producto
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
