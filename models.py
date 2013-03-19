import datetime


class Compra:
    """
    """

    def __init__(self, prenda, cliente)
        self.fecha = datetime.date.today()
        self.prenda = prenda
        self.cliente = cliente


class Entrega:
    """
    """

    def __init__(self, monto)
        self.monto = monto
        self.fecha = datetime.date.today()




class Cliente:
    """
    """

    def __init__(self, dni, nombre, telefono, email)
        self._dni = dni
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.fecha_ultima_entrega = ""
        self.compras = []
        self.entregas = []


class Prenda:
    """
    """

    def __init___(self, codigo, nombre, talle, costo, precio, descripcion)
        self._codigo = codigo
        self.nombre = nombre
        self.talle = talle
        self.costo = costo
        self.precio = precio
        self. descripcion = descripcion
        self.vendida = False
        self.condicional = False
        self.pagada = False


class ListaClientes:


    def __init__(self)
        self._clientes = []


class ListaPrendas:


    def __init__(self)
        self._prendas = []


