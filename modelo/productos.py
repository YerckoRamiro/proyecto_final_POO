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
        # se valida antes de super() para que el error diga lo que de verdad pasa
        if len(productos) < Combo.MIN_PRODUCTOS:
            raise ValueError(f"Un combo necesita al menos {Combo.MIN_PRODUCTOS} productos")
        # Opcion 1: al padre le pasamos la suma inicial (asi valida precio > 0),
        # pero el precio real del combo se calcula en vivo en calcular_precio()
        suma = 0
        for producto in productos:
            suma = suma + producto.calcular_precio()
        super().__init__(nombre, suma)
        self._productos = []
        for producto in productos:
            self.agregar_producto(producto)

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
        # si el producto ya me contiene (directa o indirectamente), agregarlo haria un ciclo
        if producto.contiene_a(self):
            raise ValueError("Un combo no puede contenerse a si mismo")
        for linea in self._productos:
            if linea.producto is producto:
                linea.cantidad = linea.cantidad + cantidad
                return
        self._productos.append(ComboProducto(producto, cantidad))

    def quitar_producto(self, producto):
        for linea in self._productos:
            if linea.producto is producto:
                if self.contar_productos() - linea.cantidad < Combo.MIN_PRODUCTOS:
                    raise ValueError(f"Un combo no puede quedar con menos de {Combo.MIN_PRODUCTOS} productos")
                self._productos.remove(linea)
                return
        raise ValueError(f"{producto.nombre} no esta en el combo")

    def contar_productos(self):
        # se cuentan unidades: 2 silpanchos = 2 productos (ver SUPUESTO arriba)
        total = 0
        for linea in self._productos:
            total = total + linea.cantidad
        return total

    def calcular_precio(self):
        # cada hijo calcula su propio precio, aunque sea otro combo (polimorfismo)
        suma = 0
        for linea in self._productos:
            suma = suma + linea.calcular_precio()
        if self.contar_productos() >= self._min_producto:
            suma = suma * (1 - self._descuento)
        return round(suma, 2)

    def esta_disponible(self, dia):
        # disponible solo si todos sus productos lo estan
        for linea in self._productos:
            if not linea.producto.esta_disponible(dia):
                return False
        return True

    def contar_platos(self):
        # los platos dentro del combo pagan envase; las bebidas suman 0
        total = 0
        for linea in self._productos:
            total = total + linea.contar_platos()
        return total

    def contiene_a(self, producto):
        if self is producto:
            return True
        # busca en los hijos; si un hijo es combo, el busca en los suyos
        for linea in self._productos:
            if linea.producto.contiene_a(producto):
                return True
        return False
