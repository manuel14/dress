import wx
import models
import views
import data
import datetime
from wx.lib.pubsub import Publisher as pub
import cPickle as pickle

from views.MainFrame import MainFrame

class AppController:
    """
    Controlador principal de la app.
    """

    def __init__(self, app):

        self.app = app
        self.data = data.load()

	self.clientes = self.data['clientes']

    	self.main_window = MainFrame(None, -1, "A&M Moda")

    	self.initUi()

    	self.main_window.Show()


    def initUi(self):

        # Cargar las listas principales, lista_clientes y lista_prendas
        # =============================================================

        # lista_clientes	
        lista_clientes = self.main_window.lista_clientes

        # Agregar columnas a lista_clientes
        lista_clientes.InsertColumn(0, "DNI", width=100)
        lista_clientes.InsertColumn(1, "Nombre", width=300)
        lista_clientes.InsertColumn(2, "Telefono", width=200)
        lista_clientes.InsertColumn(3, "Saldo")

        # Agregar items a lista_clientes
        for item in self.clientes.getClientes():

            idx = lista_clientes.GetItemCount()
            lista_clientes.InsertStringItem(idx, "%s" % item.getDni()) 
            lista_clientes.SetStringItem(idx, 1, "%s" % item.getNombre()) 
            lista_clientes.SetStringItem(idx, 2, "%s" % item.getTelefono()) 
            lista_clientes.SetStringItem(idx, 3, "%s" % item.getSaldo()) 
	

    def connectEvent(self):
        
        # pestania prendas
        self.main_window.boton_detalle_prendas.Bind(wx.EVT_BUTTON, self.mostrarDetallePrenda)
        self.main_window.boton_eliminar_prendas.Bind(wx.EVT_BUTTON, self.eliminarPrenda)
        self.main_window.boton_nuevo_prendas.Bind(wx.EVT_BUTTON, self.nuevaPrenda)
        self.main_window.boton_agregar_quitar(wx.EVT_BUTTON, self.agregarQuitarCarrito)
        self.main_window.boton_realizar_venta(wx.EVT_BUTTON, self.realizarVenta)

        #pestania clientes
        self.main_window.boton_detalle_clientes.Bind(wx.EVT_BUTTON, self.mostrarDetalleCliente)
        self.main_window.boton_eliminar_clientes.Bind(wx.EVT_BUTTON, self.eliminarCliente)
        self.main_window.boton_nuevo_clientes.Bind(wx.EVT_BUTTON, self.nuevoCliente)


    def MostrarDetallePrenda(self):

        seleccionado = self.main_window.lista_prendas.getFocusedItem()

        try:
            item = self.main_window.lista_prendas.getItem()
        except Exception, e:
            raise
        else:
            pass
        finally:
            pass






        


if __name__=='__main__':
    
    app = wx.App(False)
    controller = AppController(app)
    app.MainLoop()

#enable o algo asi
#Controlador Detalle cliente
class DetalleClienteController:
    """
    COntrolador Detalle Cliente
    """

    def __init__(self, cliente, padre):

        self.cliente = cliente
        self.data = data.load()

        self.main_window = DetalleClienteFrame(padre, -1, "Detalle Cliente %s" %cliente.getNombre())

        self.initUi()

        self.main_window.Show()

    def initUi(self):

        # Cargar las listas Detalle_Cliente
        # =============================================================

        # lista_resumen_clientes    
        list_resumen_cliente = self.main_window.list_resumen_cliente

        # Agregar columnas a lista_resumen_cliente
        list_resumen_cliente.InsertColumn(0, "Fecha", width=100)
        list_resumen_cliente.InsertColumn(1, "Tipo", width=200)
        list_resumen_cliente.InsertColumn(2, "Codigo", width=200)
        list_resumen_cliente.InsertColumn(3, "Monto")

        # Agregar items a lista_resumen_cliente
        for item in self.cliente.getMovimientos():

            idx = list_resumen_cliente.GetItemCount()
            list_resumen_cliente.InsertStringItem(idx, "%s" % item.compra.fecha 
            list_resumen_cliente.SetStringItem(idx, 1, "%s" % item.getNombre()) 
            list_resumen_cliente.SetStringItem(idx, 2, "%s" % item.getTelefono()) 
            list_resumen_cliente.SetStringItem(idx, 3, "%s" % item.getSaldo()) 
        

#fecha, tipo:va si es condi, compra o pago...., 
#codigo prenda: el codigo pero si es pago no iene codi, 
#monto: si es condicional no tine monto


