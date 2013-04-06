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

        self.clientes = self.data.objects["clientes"]
        self.compras = self.data.objects["prendas"]
        self.carrito = Carrito()

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



    def mostrarDetallePrenda(self):

        seleccionado = self.main_window.lista_prendas.getFocusedItem()
        
        if seleccionado != -1:
            codigo_prenda = self.main_window.lista_prendas.getItem(seleccionado,0)
            prenda = self.prendas.getPrendaPorCodigo(int(codigo_prenda))
            controlador_detalle_prenda = DetallePrendaController(prenda, self.main_window)

    def eliminarPrenda(self):

        seleccionado = self.main_window.lista_prendas.getFocusedItem()

        if seleccionado != -1:
            codigo_prenda = self.main_window.lista_prendas.getItem(seleccionado,0)
            prenda = self.prendas.getPrendaPorCodigo(int(codigo_prenda))
            
            try:
                self.prendas.deletePrenda(prenda)
            except NameError:
                error_dialog = wx.MessageDialog(self, "No puede eliminar una prenda vendida o en condicional", "Advertencia", wx.ICON_INFORMATION)
                error_dialog.ShowModal()
                error_dialog.Destroy()
                self.Close()



    def nuevaPrenda(self):

        #recibe self para poder agregar la prenda a la lista prendas. Self.main_window es la ventana padre
        controlador_nueva_prenda = NuevaPrendaController(self, self.main_window)

    def agregarQuitarCarrito(self):
        
        seleccionado = self.main_window.lista_prendas.getFocusedItem()

        if seleccionado != -1:
            codigo_prenda = self.main_window.lista_prendas.getItem(seleccionado,0)
            prenda = self.prendas.getPrendaPorCodigo(int(codigo_prenda))
            
            try:
                carrito.addOrDeletePrenda(prenda)
            except NameError:
                error_dialog = wx.MessageDialog(self, "No puede vender una prenda vendida o en condicional", "Advertencia", wx.ICON_INFORMATION)
                error_dialog.ShowModal()
                error_dialog.Destroy()
                self.Close()

    def realizarVenta(self):
        if self.carrito.getPrendas().length() != 0:
            controlador_venta = Venta_Controller(self.carrito, self.main_window)
        else:
            error_dialog = wx.MessageDialog(self, "Seleccione al menos una prenda para vender", "Advertencia", wx.ICON_INFORMATION)
            error_dialog.ShowModal()
            error_dialog.Destroy()
            self.Close()

    def mostrarDetalleCliente(self):

        seleccionado = self.main_window.lista_clientes.getFocusedItem()
        
        if seleccionado != -1:
            dni = self.main_window.lista_clientes.getItem(seleccionado,0)
            cliente = self.clientes.getClientePorDni(dni)
            controlador_detalle_cliente = DetalleClienteController(cliente, self.main_window)        

    def eliminarCliente(self):

        seleccionado = self.main_window.lista_clientes.getFocusedItem()
        
        if seleccionado != -1:
            dni = self.main_window.lista_clientes.getItem(seleccionado,0)
            cliente = self.clientes.getClientePorDni(dni)
            self.clientes.deleteCliente(cliente)
            


    def nuevoCliente(self):
        #recibe self para poder agregar la prenda a la lista clientes
        controlador_nuevo_cliente = NuevoClienteController(self, self.main_window)




if __name__=='__main__':
    
    app = wx.App(False)
    controller = AppController(app)
    app.MainLoop()

