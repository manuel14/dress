import datetime
import string
import wx
from wx.lib.pubsub import Publisher as pub

class Compra:
    """
    """

    def __init__(self, prenda, cliente, precio, nombrePrenda):
        self.fecha = datetime.date.today()
        self.prenda = prenda
        self.nombrePrenda = nombrePrenda
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
        self.__dni = dni
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

        for compra in self.compras:
            movim = Movimiento(compra.fecha, "Compra", compra.prenda + compra.nombrePrenda, compra.precio)
            movimientos.append(movim)

        for entrega in self.entregas:
            movim = Movimiento(entrega.fecha, "Entrega", "-", entrega.monto)
            movimientos.append(movim)


        for condicional in self.condicionales:
            movim = Movimiento(condicional.fecha, "Condicional", condicional.prenda + compra.nombrePrenda, 0)
            movimientos.append(movim)

        movimientos.sort()

        return movimientos

    def getSaldo(self):
        deuda = 0
        credito = 0

        for compra in self.compras:
            deuda = deuda + compra.precio

        for entrega in self.entregas:
            credito = credito + entrega.monto

        saldo = credito - deuda

        return saldo
    
    def getEstadoCliente(self):
        # no se como hacer la comparacion entre fechas, la idea es que si getSaldo = 0
        # o fecha_ultima_entrega es menor a un mes,  que sea "al dia", si getSaldo > 0
        # y fecha_ultima_entrega es mayor a un mes pero menor a dos meses sea "tardio"
        # y si getSaldo > 0 fecha_ultima_entrega es mayor a dos meses sea "moroso"

    def getDni(self):
        return self.__dni


class Prenda:
    """
    """

    def __init___(self, codigo, nombre, talle, costo, precio, descripcion):
        self.__codigo = codigo
        self.nombre = nombre
        self.talle = talle
        self.costo = costo
        self.precio = precio
        self. descripcion = descripcion
        self.vendida = False
        self.condicional = False

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

    def getEstadoPrenda(self):
        estado = "disponible"
        
        if self.vendida:
            estado = "vendida"
        elif self.condicional:
            estado = "condicional"

        return estado

    def getCodigo(self):
        return self.__codigo

class ListaClientes:


    def __init__(self):
        self.__clientes = []

    def addCliente(self, cliente):
        self.__clientes.append(cliente)
        pub.sendMessaje("CLIENTE AGREGADO", self)

    def deleteCliente(self, cliente):
        self.__clientes.remove(cliente)
        pub.sendMessaje("CLIENTE ELIMINADO", self)

    def getClientes(self): 
        return self.__clientes

    def getClientesMorosos(self):
        clientes_morosos = []

        for cliente in __clientes:
            if cliente.getEstadoCliente = "moroso":
                clientes_morosos.append(cliente)

        return clientes_morosos

    def getClientesAlDia(self):
        clientes_al_dia = []

        for cliente in __clientes:
            if cliente.getEstadoCliente = "al dia":
                clientes_al_dia.append(cliente)

        return clientes_al_dia

    def getClientesTardios(self):
        clientes_tardios = []

        for cliente in __clientes:
            if cliente.getEstadoCliente = "tardio"
                clientes_tardios.append(moroso)

    def getClientePorDni(self, dni):
        clientes_encontrados = []
        
        for cliente in self.__clientes:
            if cliente.getDni() == dni:
                clientes_encontrados.append(cliente)

        return clientes_encontrados

    def getClientePorNombre(self, nombre):

        clientes_encontrados = []
    
        for cliente in self.__clientes:
            if string.find(cliente.nombre, nombre) > 0:
                clientes_encontrados.append(cliente)

        return clientes_encontrados
                

class ListaPrendas:


    def __init__(self):
        self.__prendas = []

    def addPrenda(self, prenda):
        self.__prendas.append(prenda)
        pub.sendMessaje("PRENDA AGREGADA", self)

    def deletePrenda(self, prenda):
        self.__prendas.remove(prenda)
        pub.sendMessaje("PRENDA ELIMINADA", self)

    def getPrendas(self): 
        return self.__prendas

    def getPrendasVendidas(self):
        prendas_vendidas = []

        for prenda in __prendas:
            if prenda.getEstadoPrenda = "vendida":
                prendas_vendidas.append(prenda)

        return prendas_vendidas

    def getPrendasDisponibles(self):
        prendas_disponibles = []

        for prenda in __prendas:
            if prenda.getEstadoPrenda = "disponible":
                prendas_disponibles.append(prenda)

        return prendas_disponibles

    def getPrendasCondicionales(self):
        prendas_condicionales = []

        for prenda in __prendas:
            if prenda.getEstadoPrenda = "condicional":
                prendas_condicionales.append(prenda)

        return prendas_condicionales

    def getPrendaPorCodigo(self, codigo):
        prendas_encontradas = []
        
        for prenda in self.__prendas:
            if prenda.getCodigo() == codigo:
                prendas_encontradas.append(prenda)

        return prendas_encontradas

    def getPrendaPorNombre(self, nombre):
        prendas_encontradas = []
    
        for prenda in self.__prendas:
            if string.find(prenda.nombre, nombre) > 0:
                prendas_encontradas.append(prenda)

        return prendas_encontradas





