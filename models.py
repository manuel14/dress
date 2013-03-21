import datetime
import wx
from wx.lib.pubsub import Publisher as pub

class Compra:
    """
    """

    def __init__(self, prenda, cliente, precio):
        self.fecha = datetime.date.today()
        self.prenda = prenda
        self.cliente = cliente
        self.precio = precio


class Condicional:
    """
    """

    def __init__(self, prenda, cliente):
        self.fecha = datetime.date.today()
        self.prenda = prenda
        self.cliente = cliente

class Movimiento:
    """
    """

    def __init__(self, fecha, movimiento, prenda, monto):
        self.fecha = fecha
        self.movimiento = movimiento
        self.monto = monto
        self.prenda = prenda

    def __cmp__(self, otroMov):
        resul = 0

        if (self.fecha > otroMov.fecha):
            resul = 1
        elif (self.fecha < otroMov.fecha):
            resul = (-1)

        return resul




class Entrega:
    """
    """

    def __init__(self, monto):
        self.monto = monto
        self.fecha = datetime.date.today()


class Cliente:
    """
    """

    def __init__(self, dni, nombre, telefono, email):
        self._dni = dni
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.fecha_ultima_entrega = ""
        self.compras = []
        self.entregas = []
        self.condicionales = []

    def setNombre(self, nombre):
        self.nombre = nombre
        pub.sendMessaje("CAMBIO CLIENTE", self)

    def setTelefono(self, telefono):
        self.telefono = telefono
        pub.sendMessaje("CAMBIO CLIENTE", self)

    def setEmail(self, email):
        self.email = email
        pub.sendMessaje("CAMBIO CLIENTE", self)
   
    def setFechaUltimaEntrega(self, fecha):
        self.fecha_ultima_entrega = fecha
        pub.sendMessaje("CAMBIO CLIENTE", self)

    def setEmail(self, nombre):
        self.nombre = nombre
        pub.sendMessaje("CAMBIO CLIENTE", self)

    def addCompra(self, compra):
        self.compras.append(compra)
        pub.sendMessaje("COMPRA AGREGADA", self)

    def addEntrega(self, entrega):
        self.entregas.append(entrega)
        pub.sendMessaje("ENTREGA AGREGADA", self)

    def deleteCompra(self, compra):
        self.compras.remove(compra)
        pub.sendMessaje("COMPRA ELIMINADA", self)
    
    def deleteEntrega(self, entrega):
        self.entregas.remove(entrega)
        pub.sendMessaje("ENTREGA ELIMINADA", self)

    def addCondicional(self, condicional):
        self.condicionales.append(condicional)
        pub.sendMessaje("CONDICIONAL AGREGADO", self)

    def deleteCondicionales(self):
        self.condicionales = []
        pub.sendMessaje("CONDICIONALES ELIMINADOS")

    def getMovimietos(self):
        movimientos = []

        for compra in compras:
            movim = Movimiento(compra.fecha, "Compra", compra.prenda, compra.precio)
            movimientos.append(movim)

        for entrega in entregas:
            movim = Movimiento(entrega.fecha, "Entrega", "-", entrega.monto)
            movimientos.append(movim)


        for condicional in condicionales:
            movim = Movimiento(condicional.fecha, "Condicional", condicional.prenda, 0)
            movimientos.append(movim)

        movimientos.sort()

        return movimientos


class Prenda:
    """
    """

    def __init___(self, codigo, nombre, talle, costo, precio, descripcion):
        self._codigo = codigo
        self.nombre = nombre
        self.talle = talle
        self.costo = costo
        self.precio = precio
        self. descripcion = descripcion
        self.vendida = False
        self.condicional = False
        self.pagada = False

    def setNombre(self, nombre):
        self.nombre = nombre
        pub.sendMessaje("CAMBIO PRENDA", self)

    def setTalle(self, talle):
        self.talle = talle
        pub.sendMessaje("CAMBIO PRENDA", self)

    def setCosto(self, costo):
        self.costo = costo
        pub.sendMessaje("CAMBIO PRENDA", self)
    
    def setPrecio(self, precio):
        self.precio = precio
        pub.sendMessaje("CAMBIO PRENDA", self)

    def setDescripcion(self, descripcion):
        self.descripcion = descripcion
        pub.sendMessaje("CAMBIO PRENDA", self)

    def setVendida(self, vendida):
        self.vendida = vendida
        pub.sendMessaje("CAMBIO PRENDA", self)

    def setCondicional(self, condicional):
        self.condicional = condicional
        pub.sendMessaje("CAMBIO PRENDA", self)

    def setPagada(self, pagada):
        self.pagada = pagada
        pub.sendMessaje("CAMBIO PRENDA", self)



class ListaClientes:


    def __init__(self):
        self._clientes = []


class ListaPrendas:


    def __init__(self):
        self._prendas = []


