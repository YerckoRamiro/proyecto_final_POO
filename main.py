from restaurante import Restaurante
from modelo.productos import Plato, Bebida
from modelo.pedidos import Pedido
from modelo.pagos import PagoEfectivo, PagoQr, PagoTarjeta

MENU = """
===== SABOR VALLUNO (variante D) =====
 1. Registrar producto
 2. Armar combo
 3. Listar menu de un dia
 4. Registrar cliente
 5. Crear pedido (local, para llevar, delivery)
 6. Agregar o quitar productos de un pedido
 7. Ver detalle de un pedido
 8. Cambiar estado de un pedido
 9. Cobrar pedido
10. Reporte del dia y top 3
 0. Salir"""


def cargar_datos_ejemplo(restaurante):
    silpancho = Plato("Silpancho", 35)
    pique = Plato("Pique macho", 45)
    # SUPUESTO: el chicharron solo se vende los domingos
    chicharron = Plato("Chicharron", 45, ["domingo"])
    sopa = Plato("Sopa de mani", 18)
    mocochinchi = Bebida("Mocochinchi", 6, "vaso", "refresco natural")
    gaseosa = Bebida("Coca Cola", 5, "vaso", "gaseosa")
    for producto in [silpancho, pique, chicharron, sopa, mocochinchi, gaseosa]:
        restaurante.registrar_producto(producto)
    restaurante.armar_combo("Combo clasico", [silpancho, mocochinchi])
    restaurante.registrar_cliente("Ana Rojas", "71234567", "ana@correo.com", "clave123", "Calle Sucre 10")


def mostrar_productos(productos):
    numero = 1
    for producto in productos:
        # siempre calcular_precio(): en un combo el precio se calcula en vivo
        print(f"  {numero}. {producto.nombre} - Bs {producto.calcular_precio():.2f}")
        numero = numero + 1


def elegir_producto(restaurante):
    menu = restaurante.menu
    mostrar_productos(menu)
    opcion = int(input("Numero de producto: "))
    if opcion < 1 or opcion > len(menu):
        raise ValueError("Numero de producto invalido")
    return menu[opcion - 1]


def mostrar_detalle(pedido):
    print(f"Pedido N. {pedido.numero} - {pedido.obtener_tipo()} - {pedido.estado} - dia {pedido.dia}")
    for item in pedido.items:
        print(f"  {item.cantidad} x {item.producto.nombre} = Bs {item.calcular_precio():.2f}")
    print(f"  Subtotal:  Bs {pedido.calcular_subtotal():.2f}")
    print(f"  Descuento: Bs {pedido.calcular_descuento():.2f}")
    print(f"  Cargos:    Bs {pedido.calcular_cargos():.2f}")
    print(f"  Total:     Bs {pedido.calcular_total():.2f}")


def registrar_producto(restaurante):
    tipo = input("1. Plato  2. Bebida: ").strip()
    nombre = input("Nombre: ")
    precio = float(input("Precio (Bs): "))
    if tipo == "1":
        texto = input("Dias de venta separados por coma (vacio = todos): ").strip()
        if texto == "":
            producto = Plato(nombre, precio)
        else:
            dias = []
            for dia in texto.split(","):
                dias.append(dia.strip())
            producto = Plato(nombre, precio, dias)
    elif tipo == "2":
        presentacion = input("vaso o jarra: ").strip()
        categoria = input("refresco natural o gaseosa: ").strip()
        producto = Bebida(nombre, precio, presentacion, categoria)
    else:
        raise ValueError("Opcion invalida")
    restaurante.registrar_producto(producto)
    print(f"Registrado: {producto.nombre} - Bs {producto.calcular_precio():.2f}")


def armar_combo(restaurante):
    nombre = input("Nombre del combo: ")
    cantidad = int(input("Cuantos productos tendra (minimo 2): "))
    productos = []
    for i in range(cantidad):
        productos.append(elegir_producto(restaurante))
    combo = restaurante.armar_combo(nombre, productos)
    print(f"Combo creado: {combo.nombre} - Bs {combo.calcular_precio():.2f}")


def listar_menu(restaurante):
    dia = input("Dia (lunes, martes, miercoles, jueves, viernes, sabado, domingo): ").strip().lower()
    mostrar_productos(restaurante.listar_menu(dia))


def registrar_cliente(restaurante):
    nombre = input("Nombre: ")
    celular = input("Celular (8 digitos, empieza en 6 o 7): ").strip()
    correo = input("Correo: ")
    password = input("Password: ")
    direccion = input("Direccion: ")
    cliente = restaurante.registrar_cliente(nombre, celular, correo, password, direccion)
    print(f"Cliente registrado: {cliente.nombre} ({cliente.celular})")


def crear_pedido(restaurante):
    tipo = input("1. Local  2. Para llevar  3. Delivery: ").strip()
    if tipo == "1":
        pedido = restaurante.crear_pedido_local(int(input("Mesa (1 a 15): ")))
    elif tipo == "2":
        cliente = restaurante.buscar_cliente(input("Celular del cliente: ").strip())
        pedido = restaurante.crear_pedido_para_llevar(cliente)
    elif tipo == "3":
        cliente = restaurante.buscar_cliente(input("Celular del cliente: ").strip())
        zona = input("Zona (Cercado, Quillacollo, Sacaba, Vinto): ").strip()
        direccion = input("Direccion de entrega: ")
        pedido = restaurante.crear_pedido_delivery(cliente, zona, direccion)
    else:
        raise ValueError("Opcion invalida")
    print(f"Pedido N. {pedido.numero} ({pedido.obtener_tipo()}) creado")


def agregar_o_quitar(restaurante):
    pedido = restaurante.buscar_pedido(int(input("Numero de pedido: ")))
    accion = input("1. Agregar  2. Quitar: ").strip()
    producto = elegir_producto(restaurante)
    if accion == "1":
        pedido.agregar_producto(producto, int(input("Cantidad (1 a 20): ")))
    elif accion == "2":
        pedido.quitar_producto(producto)
    else:
        raise ValueError("Opcion invalida")
    mostrar_detalle(pedido)


def ver_detalle(restaurante):
    mostrar_detalle(restaurante.buscar_pedido(int(input("Numero de pedido: "))))


def cambiar_estado(restaurante):
    pedido = restaurante.buscar_pedido(int(input("Numero de pedido: ")))
    print(f"Estado actual: {pedido.estado}")
    opcion = input("1. EN_PREPARACION  2. LISTO  3. ENTREGADO  4. CANCELAR: ").strip()
    estados = {"1": Pedido.EN_PREPARACION, "2": Pedido.LISTO, "3": Pedido.ENTREGADO}
    if opcion == "4":
        pedido.cancelar()
    elif opcion in estados:
        pedido.cambiar_estado(estados[opcion])
    else:
        raise ValueError("Opcion invalida")
    print(f"Nuevo estado: {pedido.estado}")


def cobrar(restaurante):
    numero = int(input("Numero de pedido: "))
    pedido = restaurante.buscar_pedido(numero)
    print(f"Total del pedido: Bs {pedido.calcular_total():.2f}")
    metodo = input("1. Efectivo  2. QR  3. Tarjeta (3 % de comision): ").strip()
    if metodo == "1":
        pago = PagoEfectivo(input("Monto recibido: "))
    elif metodo == "2":
        pago = PagoQr(input("Codigo de transaccion (10 digitos): "))
    elif metodo == "3":
        pago = PagoTarjeta()
    else:
        raise ValueError("Opcion invalida")
    print(restaurante.cobrar_pedido(numero, pago))


def reporte(restaurante):
    ventas = restaurante.reporte_ventas_dia()
    if len(ventas) == 0:
        print("Todavia no hay pedidos pagados hoy")
    for tipo in ventas:
        print(f"  {tipo}: {ventas[tipo]['pedidos']} pedidos, Bs {ventas[tipo]['total']:.2f}")
    print("Top 3 productos:")
    for par in restaurante.top_productos(3):
        print(f"  {par[0].nombre}: {par[1]} unidades")


def main():
    restaurante = Restaurante()
    cargar_datos_ejemplo(restaurante)
    opcion = ""
    while opcion != "0":
        print(MENU)
        opcion = input("Opcion: ").strip()
        # los errores de validacion se muestran y el programa sigue
        try:
            if opcion == "1":
                registrar_producto(restaurante)
            elif opcion == "2":
                armar_combo(restaurante)
            elif opcion == "3":
                listar_menu(restaurante)
            elif opcion == "4":
                registrar_cliente(restaurante)
            elif opcion == "5":
                crear_pedido(restaurante)
            elif opcion == "6":
                agregar_o_quitar(restaurante)
            elif opcion == "7":
                ver_detalle(restaurante)
            elif opcion == "8":
                cambiar_estado(restaurante)
            elif opcion == "9":
                cobrar(restaurante)
            elif opcion == "10":
                reporte(restaurante)
            elif opcion == "0":
                print("Hasta luego")
            else:
                print("Opcion invalida")
        except ValueError as error:
            print(f"Error: {error}")


main()
