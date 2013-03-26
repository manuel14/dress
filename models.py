import datetime
import string
import wx
from wx.lib.pubsub import Publisher as pub

class Movimiento:
    """
    Un movimiento representa alguna transaccion de productos
    y/o dinero. Sirve como base para compras, entregas, etc..
    """

    def __init__(self, cliente):

        self.fecha = datetime.date.today()
        self.cliente = cliente


    def __cmp__(self, otroMov):

        if (self.fecha > otroMov.fecha):
            return 1
        elif (self.fecha < otroMov.fecha):
            return -1
        else: 
            return 0



class Pago(Movimiento):
    """
    Un pago es una entrega de dinero en cualquier concepto. Ya sea
    en una Compra (en concepto de entrega) o saldar una deuda.
    """

    def __init__(self, monto, cliente):

        Movimiento.__init__(self, cliente)
        self.monto = monto



class Compra(Movimiento):
    """
    Una compra representa un movimiento en el cual se realiza el
    pago parcial o completo de una prenda por parte de un cliente. 
    Y se retira el producto.
    """

    def __init__(self, monto, prenda, nombre_prenda, cliente):

        Movimiento.__init__(self, cliente)
        self.prenda = prenda
        self.monto = monto
        self.nombre_prenda = nombre_prenda



class Condicional(Movimiento):
    """
    Un concepto de la magia villangelense, donde una persona puede 
    llevar una prenda y decidir si lo va a comprar luego. Sino devuelve la
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

        self._pagos.append(pago)
        pub.sendMessaje("PAGO_AGREGADO", self)


    def deleteCompra(self, compra):

        self._compras.remove(compra)
        pub.sendMessaje("COMPRA_ELIMINADA", self)

    
    def deletePagos(self, pago):

        self._pagos.remove(pago)
        pub.sendMessaje("PAGO_ELIMINADO", self)


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
            return "al_dia"
        else:
            
            if delta > 60:
                return "moroso"
            else:
                return "tardio"

    def getNombre(self):
        
        return self._nombre  

    def getTelefono(self):
        
        return self._telefono

    def getEmail(self):

        return self._email

class Prenda:
    """
    Representa una prenda de ropa. El producto del negocio.
    """

    _index = 0 # Lleva la cuenta de los codigos de las prendas

    def __init__(self, nombre, talle, costo, precio):

        self._codigo = Prenda._index #el codigo se autoasigna con el valor de _index
        Prenda._index += 1

        self.nombre = nombre
        self.talle = talle
        self.costo = costo
        self.precio = precio
        self.descripcion = descripcion

        self._vendida = False
        self._condicional = False


    def setNombre(self, nombre):

        self.nombre = nombre
        pub.sendMessaje("CAMBIO_PRENDA", self)


    def setTalle(self, talle):

        self.talle = talle
        pub.sendMessaje("CAMBIO_PRENDA", self)


    def setCosto(self, costo):

        self.costo = costo
        pub.sendMessaje("CAMBIO_PRENDA", self)

    
    def setPrecio(self, precio):
    
        self.precio = precio
        pub.sendMessaje("CAMBIO_PRENDA", self)


    def setDescripcion(self, descripcion):

        self.descripcion = descripcion
        pub.sendMessaje("CAMBIO_PRENDA", self)


    def setVendida(self, vendida):

        self.vendida = vendida
        pub.sendMessaje("CAMBIO_PRENDA", self)


    def setCondicional(self, condicional):

        self.condicional = condicional
        pub.sendMessaje("CAMBIO_PRENDA", self)
    

    def getEstado(self):

        estado = "disponible"
        
        if self.vendida:
            estado = "vendida"
        elif self.condicional:
            estado = "condicional"

        return estado

    def getCodigo(self):

        return self._codigo



class ListaClientes:
    """
    Coleccion de instancias de Cliente
    """

    def __init__(self):

        self._clientes = []


    def addCliente(self, cliente):

        self._clientes.append(cliente)
        pub.sendMessaje("CLIENTE_AGREGADO", self)


    def deleteCliente(self, cliente):

        self._clientes.remove(cliente)
        pub.sendMessaje("CLIENTE_ELIMINADO", self)


    def getClientes(self): 

        return self._clientes
    

    def getClientesPorEstado(self, estado):
        
        return filter(lambda c:c.getEstado()==estado, self._clientes)


    def getClientesMorosos(self):

    return self.getClientesPorEstado('moroso')


    def getClientesAlDia(self):

    return self.getClientesPorEstado('al_dia')


    def getClientesTardios(self):

    return self.getClientesPorEstado('tardio')


    def getClientePorDni(self, dni):

        return filter(lambda c:c._dni==dni, self._clientes)


    def findClientePorNombre(self, nombre):

        return filter(lambda c:string.find(string.lower(c.getNombre()), string.lower(nombre)) >= 0, self._clientes)
                


class ListaPrendas:
    """
    Coleccion de instancias de Prenda.
    """

    def __init__(self):

        self._prendas = []


    def addPrenda(self, prenda):

        self._prendas.append(prenda)
        pub.sendMessaje("PRENDA_AGREGADA", self)
    

    def deletePrenda(self, prenda):

        self._prendas.remove(prenda)
        pub.sendMessaje("PRENDA_ELIMINADA", self)


    def getPrendas(self): 
    
        return self._prendas


    def getPrendasVendidas(self):

        return filter(lambda p:p.vendida, self._prendas)


    def getPrendasDisponibles(self):

        return filter(lambda p:p.getEstado()=='disponible', self._prendas)


    def getPrendasCondicionales(self):

        return filter(lambda p:p.condicional, self._prendas)


    def getPrendaPorCodigo(self, codigo):

        return filter(lambda p:p.getCodigo()==codigo, self._prendas)


    def findPrendaPorNombre(self, nombre):

        return filter(lambda p:string.find(string.lower(p.nombre), string.lower(nombre)) >= 0, self._prendas)



class Carrito:
    """
    Almacena terporalmente las prendas antes de realizar la venta
    """

    def __init__(self):

        self._prendas = []


    def addPrenda(self, prenda):

        self._prendas.append(prenda)
        pub.sendMessaje("PRENDA_AGREGADA_CARRITO", self)
    

    def deletePrenda(self, prenda):

        self._prendas.remove(prenda)
        pub.sendMessaje("PRENDA_ELIMINADA_CARRITO", self)


    def getPrendas(self): 
    
        return self._prendas
