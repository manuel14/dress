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

        self.configuracion = self.data.objects["configuracion"]


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
        
        # pestania prendas eventos
        self.main_window.boton_detalle_prendas.Bind(wx.EVT_BUTTON, self.mostrarDetallePrenda)
        self.main_window.boton_eliminar_prendas.Bind(wx.EVT_BUTTON, self.eliminarPrenda)
        self.main_window.boton_nuevo_prendas.Bind(wx.EVT_BUTTON, self.nuevaPrenda)
        self.main_window.boton_agregar_quitar.Bind(wx.EVT_BUTTON, self.agregarQuitarCarrito)
        self.main_window.boton_realizar_venta.Bind(wx.EVT_BUTTON, self.realizarVenta)

        self.main_window.texto_buscar_prendas.Bind(wx.EVT_SET_FOCUS, self.onSetFocusBuscarPrendas)
        self.main_window.texto_buscar_prendas.Bind(wx.KILL_FOCUS, self.onKillFocusBuscarPrendas)
        self.main_window.texto_buscar_prendas.Bind(wx.EVT_TEXT_ENTER, self.buscarPrendas)


        #pestania clientes eventos
        self.main_window.boton_detalle_clientes.Bind(wx.EVT_BUTTON, self.mostrarDetalleCliente)
        self.main_window.boton_eliminar_clientes.Bind(wx.EVT_BUTTON, self.eliminarCliente)
        self.main_window.boton_nuevo_clientes.Bind(wx.EVT_BUTTON, self.nuevoCliente)

        self.main_window.texto_buscar_clientes.Bind(wx.EVT_SET_FOCUS, self.onSetFocusBuscarClientes)
        self.main_window.texto_buscar_clientes.Bind(wx.KILL_FOCUS, self.onKillFocusBuscarClientes)
        self.main_window.texto_buscar_prendas.Bind(wx.EVT_TEXT_ENTER, self.buscarClientes)

        #suscripcion a eventos de Cliente
        pub.subscribe(self.actualizarCliente, "CAMBIO_CLIENTE")
        pub.subscribe(self.actualizarCliente, "COMPRA_AGREGADA")
        pub.subscribe(self.actualizarCliente, "PAGO_AGREGADO")
        pub.subscribe(self.actualizarCliente, "COMPRA_ELIMINADA")
        pub.subscribe(self.actualizarCliente, "PAGO_ELIMINADO")

        #suscripcion a eventos de Prenda
        pub.subscribe(self.actualizarPrenda, "CAMBIO_PRENDA")

        #suscripcion a eventos de ListaClientes
        pub.subscribe(self.clienteAgregado, "CLIENTE_AGREGADO")
        pub.suscribe(self.clienteEliminado, "CLIENTE_ELIMINADO")

        #suscripcion a eventos de ListaPrendas
        pub.suscribe(self.prendaAgregada, "PRENDA_AGREGADA")
        pub.suscribe(self.prendaEliminada, "PRENDA_ELIMINADA")

        #suscripcion a eventos de Configuracion
        pub.suscribe(self.actualizadaConfiguracionPrendas, "CONFIGURACION_PRENDAS_CAMBIO")
        pub.suscribe(self.actualizadaConfiguracionclientes, "CONFIGURACION_CLIENTES_CAMBIO")


    #metodos de la pestania prendas
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

    def onSetFocusBuscarPrendas(self):
        self.main_window.texto_buscar_prendas.Clear()

    def onKillFocusBuscarPrendas(self):
        self.main_window.texto_buscar_prendas.SetValue('Buscar...')

    def buscarPrendas(self):
        seleccionado = self.main_window.radio_box_prendas.GetSelection()
        prendas_activas = self.prendas.getPrendasActivas(self.configuracion)
        value = self.main_window.texto_buscar_prendas.GetValue()
        lista_a_cargar = ListaPrendas()

        if seleccionado == 0:
            prenda_buscada = prendas_activas.getPrendaPorCodigo(value)
            #como solo devuelve un elemnto lo agrego a la lista
            lista_a_cargar.addPrenda(prenda_buscada)

        elif seleccionado == 1:
            prenda_buscada = prendas_activas.findPrendaPorNombre(value)
            #como devuelve mas de un elemento los agrego con un for
            for prenda in prenda_buscada:
                lista_a_cargar.addPrenda(prenda)

        self.cargarListaPrendas(lista_a_cargar)


    
    #metodos de la pestania clientes

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

    def onSetFocusBuscarClientes(self):
        self.main_window.texto_buscar_clientes.Clear()

    def onKillFocusBuscarClientes(self):
        self.main_window.texto_buscar_clientes.SetValue('Buscar...')

    def buscarClientes(self):
        seleccionado = self.main_window.radio_box_clientes.GetSelection()
        clientes_activos = self.clientes.getClientesActivos(self.configuracion)
        value = self.main_window.texto_buscar_clientes.GetValue()
        lista_a_cargar = ListaClientes()

        if seleccionado == 0:
            cliente_buscado = clientes_activos.getClientePorDni(value)
            #como solo devuelve un elemnto lo agrego a la lista
            lista_a_cargar.addCliente(cliente_buscado)

        elif seleccionado == 1:
            cliente_buscado = clientes_activos.findClientePorNombre(value)
            #como devuelve mas de un elemento los agrego con un for
            for cliente in cliente_buscado:
                lista_a_cargar.addCliente(cliente)

        self.cargarListaClientes(lista_a_cargar)


    #metodos de suscripcion a eventos
    def actualizarCliente(self, message):
        #este metodo debe actualizar en la lista clientes el cliente
        #debe buscarlo en la tabla y modificarlo, no olvidar que ademas
        #de modificar los datos se debe modificar su estado (color)
        pass

    def actualizarPrenda(self,message):
        #este metodo debe actualizar en la lista prendas la prenda
        #debe buscarla en la tabla y modificarla, no olvidar que ademas
        #de modificar los datos se debe modificar su estado (color)
        pass

    def clienteAgregado(self, message):
        #este metodo debe agregar el cliente, posiblemente use el mismo 
        #que se utiliza para cargar los elemenotos a la lista
        pass

    def clienteEliminado(self, message):
        #este metodo debe eliminar el cliente de la lista
        pass

    def prendaAgregada(self, message):
        #este metodo debe agregar la prenda, posiblemente use el mismo 
        #que se utiliza para cargar los elemenotos a la lista
        pass

    def prendaEliminada(self, message):
        #este metodo debe eliminar la prenda de la lista
        pass

    def actualizadaConfiguracionPrendas(self, message):
        #debe recargar la lista de prendas, con la nueva configuracion

    def actualizadaConfiguracionClientes(self, message):
        #debe recargar la lista de clientes, con la nueva configuracion

if __name__=='__main__':
    
    app = wx.App(False)
    controller = AppController(app)
    app.MainLoop()

