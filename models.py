import datetime
import string
import wx
from wx.lib.pubsub import Publisher as pub

class Movimiento:
    """
    Un movimiento representa alguna transaccion de productos
    y/o dinero. Sirve como base para compras, entregas, etc..
    """

    def __init__(self, cliente, fecha=datetime.date.today()):

        self.fecha = fecha
	self.cliente = cliente


    def __cmp__(self, otroMov):

        if (self.fecha > otroMov.fecha):
	    return 1
        elif (self.fecha < otroMov.fecha):
	    return -1



class Pago(Movimiento):
    """
    Un pago es una entrega de dinero en cualquier concepto. Ya sea
    en una Compra, para saldar un Condicional, o saldar una deuda.
    """

    def __init__(self, monto, cliente):

        Movimiento.__init__(self, cliente)
        self.monto = monto



class Compra(Movimiento):
    """
    Una compra representa un movimiento en el cual se realiza el
    pago completo de una prenda. Y se retira el producto.
    Se asume que en una Compra se debe entregar algo de dinero,
    de otro modo seria un Condicional en vez de un a Compra.
    """

    def __init__(self, monto,  prenda, cliente):

        Movimiento.__init__(self, cliente)
        self.prenda = prenda
	self.pago = Pago(monto); # Sera que se pueden hacer varios pagos?



class Condicional(Movimiento):
    """
    Un concepto villangelense, donde una persona puede llevar una 
    prenda y decidir si lo va a comprar luego. Sino devuelve la
    prenda.
    """

    def __init__(self, prenda, cliente):
        
	Movimiento.__init__(self, cliente)
        self.prenda = prenda



class Cliente:
    """
    Representa a un Cliente, y contiene su informacion.
    """

    def __init__(self, dni, nombre, telefono, email):

        self._dni = dni
        self._nombre = nombre
        self._telefono = telefono
        self._email = email

        self._compras = []
        self._pagos = []
        self._condicionales = []


    def setNombre(self, nombre):

        self._nombre = nombre
        pub.sendMessaje("CAMBIO_CLIENTE", self)


    def setTelefono(self, telefono):

        self._telefono = telefono
        pub.sendMessaje("CAMBIO_CLIENTE", self)


    def setEmail(self, email):

        self._email = email
        pub.sendMessaje("CAMBIO_CLIENTE", self)

   
    def addCompra(self, compra):

        self._compras.append(compra)
        pub.sendMessaje("COMPRA_AGREGADA", self)


    def addPagos(self, pago):

        self._pagos.append(entrega)
        pub.sendMessaje("ENTREGA_AGREGADA", self)


    def deleteCompra(self, compra):

        self._compras.remove(compra)
        pub.sendMessaje("COMPRA_ELIMINADA", self)

    
    def deletePagos(self, entrega):

        self._pagos.remove(entrega)
        pub.sendMessaje("ENTREGA_ELIMINADA", self)


    def addCondicional(self, condicional):

        self._condicionales.append(condicional)
        pub.sendMessaje("CONDICIONAL_AGREGADO", self)


    def deleteCondicionales(self):

        self._condicionales = []
        pub.sendMessaje("CONDICIONALES_ELIMINADOS")


    def getDni(self):

        return self._dni


    def getMovimietos(self):

        movimientos = self._compras + self._pagos + self._condicionales
        movimientos.sort()

        return movimientos


    def getSaldo(self):

        deuda = 0
        credito = 0

        for compra in self._compras:
            deuda += compra.prenda.precio

        for pagos in self._pagos:
            credito += pago.monto

        return (credito - deuda)


    def getUltimoPago(self):

        return max(self._pagos, key= lambda x:x.fecha)

    
    def getEstado(self):

        # La cantidad de dias en la cual se debe realizar un pago
    	plazo = datetime.timedelta(days=30)

	# Cantidad de dias desde que hizo el ultimo pago hasta hoy
	delta = (datetime.date.today() - self.getUltimoPago().fecha).days

	en_plazo = delta < 30

	if self.getSaldo() == 0 or en_plazo:
	    return "al dia"
	else:
	    
	    if delta > 60:
	        return "moroso"
	    else:
	        return "tardio"



# Refactorizado hasta aqui.
# -------------------------


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





