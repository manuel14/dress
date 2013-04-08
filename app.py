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
        
        #vinculacion pestania prendas eventos
        self.main_window.boton_detalle_prendas.Bind(wx.EVT_BUTTON, self.mostrarDetallePrenda)
        self.main_window.boton_eliminar_prendas.Bind(wx.EVT_BUTTON, self.eliminarPrenda)
        self.main_window.boton_nuevo_prendas.Bind(wx.EVT_BUTTON, self.nuevaPrenda)
        self.main_window.boton_agregar_quitar.Bind(wx.EVT_BUTTON, self.agregarQuitarCarrito)
        self.main_window.boton_realizar_venta.Bind(wx.EVT_BUTTON, self.realizarVenta)

        self.main_window.texto_buscar_prendas.Bind(wx.EVT_SET_FOCUS, self.onSetFocusBuscarPrendas)
        self.main_window.texto_buscar_prendas.Bind(wx.KILL_FOCUS, self.onKillFocusBuscarPrendas)
        self.main_window.texto_buscar_prendas.Bind(wx.EVT_TEXT_ENTER, self.buscarPrendas)


        #viculacion pestania clientes eventos
        self.main_window.boton_detalle_clientes.Bind(wx.EVT_BUTTON, self.mostrarDetalleCliente)
        self.main_window.boton_eliminar_clientes.Bind(wx.EVT_BUTTON, self.eliminarCliente)
        self.main_window.boton_nuevo_clientes.Bind(wx.EVT_BUTTON, self.nuevoCliente)

        self.main_window.texto_buscar_clientes.Bind(wx.EVT_SET_FOCUS, self.onSetFocusBuscarClientes)
        self.main_window.texto_buscar_clientes.Bind(wx.KILL_FOCUS, self.onKillFocusBuscarClientes)
        self.main_window.texto_buscar_prendas.Bind(wx.EVT_TEXT_ENTER, self.buscarClientes)

        #vinculacion eventos menu

        self.main_window.realizar_backup.Bind(wx.EVT_MENU, self.realizarBackup)
        self.main_window.restaurar_backup.Bind(wx.EVT_MENU, self.restaurarBackup) 
        self.main_window.ver_disponibles.Bind(wx.EVT_MENU, self.verDisponibles) 
        self.main_window.ver_condicionales.Bind(wx.EVT_MENU, self.verCondicionales) 
        self.main_window.ver_vendidas.Bind(wx.EVT_MENU, self.verVendidas)
        self.main_window.ver_al_dia.Bind(wx.EVT_MENU, self.verAlDia) 
        self.main_window.ver_tardios.Bind(wx.EVT_MENU, self.verTardios) 
        self.main_window.ver_morosos.Bind(wx.EVT_MENU, self.verMorosos) 
        self.main_window.vaciar_carrito.Bind(wx.EVT_MENU, self.vaciarCarrito)
        self.main_window.borrar_todo.Bind(wx.EVT_MENU, self.borrarTodo) 
        self.main_window.informe_lista_correos.Bind(wx.EVT_MENU, self.listaCorreos)
        self.main_window.informe_lista_correos_morosos.Bind(wx.EVT_MENU, self.listaCorreosMorosos) 
        self.main_window.informe_lista_telefonos.Bind(wx.EVT_MENU, self.listaTelefonos) 
        self.main_window.informe_lista_telefonos_morosos.Bind(wx.EVT_MENU, self.listaTelefonosMorosos)
        self.main_window.informe_lista_cumpleanios_mes.Bind(wx.EVT_MENU, self.listaCumpleaniosMes)
        self.main_window.informe_totales.Bind(wx.EVT_MENU, self.informeTotales)
        
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

        #suscripcion a eventos carrito
        pub.suscribe(self.prendaAgregadaCarrito, "PRENDA_AGREGADA_CARRITO")
        pub.suscribe(self.prendaEliminadaCarrito, "PRENDA_ELIMINADA_CARRITO")
        pub.suscribe(self.carritoVaciado, "CARRITO_VACIADO")
        

    #metodos de la pestania prendas----------------------------------------------

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


    
    #metodos de la pestania clientes---------------------------------------------

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


    #metodos de suscripcion a eventos--------------------------------------------
    def actualizarCliente(self, message):
        #este metodo debe actualizar en la lista clientes el cliente
        #debe buscarlo en la tabla y modificarlo, no olvidar que ademas
        #de modificar los datos se debe modificar su estado (color)
        pass

    def actualizarPrenda(self, message):
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

    def prendaAgregadaCarrito(self, message):
        #este metodo debe cambiar el color de la prenda agregada

    def prendaEliminadaCarrito(self, message):
        #este metodo debe cambiar el color de la prenda eliminada

    def carritoVaciado(self, message):
        #este metodo debe recargar las prendas activas

    #metodos barra menu------------------------------------------------------------

    def realizarBackup(self):
        
        # Abrir dialogo para seleccionar ruta de destino del archivo de backup
        file_dialog = wx.FileDialog(self, style = wx.SAVE)
        d = datetime.date.today()
        filename = "%s-%s-%s-backup.bak" % (d.day, d.month, d.year)
        file_dialog.SetFilename(filename)
        file_dialog.SetWildcard("Archivos de Backup (*.bak)|*.bak|Todos los archivos (*.*)|*.*")
        if file_dialog.ShowModal() == wx.ID_OK:
                data.backup(file_dialog.GetPath())
                msgbox = wx.MessageDialog(self, "Archivo de backup creado satisfactoriamente.", "INFO", style=wx.ICON_INFORMATION)
                msgbox.ShowModal()

    def restaurarBackup(self):
        #leo copia del sgpd vos que entendes tu codigo jaja
    
    def verDisponibles(self):
        self.main_window.configuracion.setMostrarDisponibes(self.ver_disponibles.IsChecked())        

    def verCondicionales(self):
        self.main_window.configuracion.setMostrarCondicionales(self.ver_condicionales.IsChecked())

    def verVendidas(self):
        self.main_window.configuracion.setMostrarVendidas(self.ver_vendidas.IsChecked())

    def verAlDia(self):
        self.main_window.configuracion.setMostrarAlDia(self.ver_al_dia.IsChecked())

    def verTardios(self):
        self.main_window.configuracion.setMostrarTardios(self.ver_tardios.IsChecked())

    def verMorosos(self):
        self.main_window.configuracion.setMostrarMorosos(self.ver_morosos.IsChecked())    
    
    def vaciarCarrito(self):
        self.carrito.vaciarCarrito()

    def borrarTodo(self):
        #este metodo debe borrar el archivo con los objetos serializados
        pass

    def listaCorreos(self):
        correos = ''

        for cliente in clientes.getClientes():
            correos = correos + cliente.getEmail() + ';'

        #se debe instanciar la ventana que contenga la lista

    def listaCorreosMorosos(self):
        correos = ''

        for cliente in clientes.getClientesMorosos():
            correos = correos + cliente.getEmail() + ';'

        #se debe instanciar la ventana que contenga la lista

    def listaTelefonos(self):

        datosNecesarios = {'dni': '', 'nombre': '', 'tel': ''}
        lista_telefonos_clientes = []

        for cliente in clientes.getClientes():
            datosNecesarios['dni'] = cliente.getDni()
            datosNecesarios['nombre'] = cliente.getNombre()
            datosNecesarios['tel'] = cliente.getTel()
            lista_telefonos_clientes.append(datosNecesarios)

        #se debe instanciar la ventana que contenga los telefonos

    def listaTelefonosMorosos(self):
        
        datosNecesarios = {'dni': '', 'nombre': '', 'tel': ''}
        lista_telefonos_clientes = []

        for cliente in clientes.getClientesMorosos():
            datosNecesarios['dni'] = cliente.getDni()
            datosNecesarios['nombre'] = cliente.getNombre()
            datosNecesarios['tel'] = cliente.getTel()
            lista_telefonos_clientes.append(datosNecesarios)

        #se debe instanciar la ventana que contenga los telefonos        

    def listaCumpleaniosMes(self):
        cumpleanieros = []

        for cliente in clientes.getClientes():
            if cliente.cumpleAniosEsteMes():
                cumpleanieros.append(cliente)

        #se debe instanciar la ventana que contenga los clientes    


    def informeTotales(self):
        total_ganancias = 0
        total_deuda = 0
        total_capital_en_prendas = 0
        total_inversion = 0


        for prenda in prendas:
            
            total_inversion += prenda.precio

            if prenda.getEstado() == 'vendida'
                total ganancias += (prenda.precio - prenda.costo)

            if (prenda.getEstado() == 'disponible') or (prenda.getEstado() == 'condicional'):
                total_capital_en_prendas += prenda.precio

        for cliente in clientes:

            total_deuda += cliente.getSaldo()

        #se debe instanciar la ventana que tiene los totales







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
            if isinstance(item, Compra):
                list_resumen_cliente.InsertStringItem(idx, "%s" % item.movimiento.fecha)
                list_resumen_cliente.SetStringItem(idx, 1, "Compra" 
                list_resumen_cliente.SetStringItem(idx, 2, "%s" % item.Prenda.getCodigo) 
                list_resumen_cliente.SetStringItem(idx, 3, "%s" % item.getSaldo())                
            elif isinstance(movimiento, Pago):
                cliente_casual.addPago(movimiento)


            list_resumen_cliente.InsertStringItem(idx, "%s") #/%s/%s" % (datetime.date.today().day, datetime.date.today().month, datetime.date.today().year)
            list_resumen_cliente.SetStringItem(idx, 1, "%s" % item.getNombre()) 
            list_resumen_cliente.SetStringItem(idx, 2, "%s" % item.getTelefono()) 
            list_resumen_cliente.SetStringItem(idx, 3, "%s" % item.getSaldo()) 
        

#fecha, tipo:va si es condi, compra o pago...., 
#codigo prenda: el codigo pero si es pago no iene codi, 
#monto: si es condicional no tine monto


