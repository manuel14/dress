import wx
import models
import views
import data
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
	for item lista_clientes.getClientes():
	    
            lista_clientes
	
    def connectEvent(self):
        
        #pestaña prendas
        self.main_window.boton_detalle_prendas.Bind(wx.EVT_BUTTON, self.mostrarDetallePrenda)
        self.main_window.boton_eliminar_prendas.Bind(wx.EVT_BUTTON, self.eliminarPrenda)
        self.main_window.boton_nuevo_prendas.Bind(wx.EVT_BUTTON, self.nuevaPrenda)
        self.main_window.boton_agregar_quitar(wx.EVT_BUTTON, self.agregarQuitarCarrito)
        self.main_window.boton_realizar_venta(wx.EVT_BUTTON, self.realizarVenta)

        #pestaña clientes
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
class DetalleCLienteController:
    """
    COntrolador Detalle Cliente
    """

    def __init__(self, cliente):

        self.cliente = cliente
        self.data = data.load()

        self.main_window = MainFrame(None, -1, "A&M Moda")

        self.initUi()

        self.main_window.Show()

    def initUi(self):

        # Cargar las listas Detalle_Cliente
        # =============================================================

        # lista_clientes    
        lista_clientes = self.main_window.lista_clientes

        # Agregar columnas a lista_clientes
        lista_clientes.InsertColumn(0, "DNI", width=100)
        lista_clientes.InsertColumn(1, "Nombre", width=300)
        lista_clientes.InsertColumn(2, "Telefono", width=200)
        lista_clientes.InsertColumn(3, "Saldo")

        # Agregar items a lista_clientes
        for item lista_clientes.getClientes():
        
            lista_clientes

#fecha, tipo:va si es condi, compra o pago...., 
#codigo prenda: el codigo pero si es pago no iene codi, 
#monto: si es condicional no tine monto


