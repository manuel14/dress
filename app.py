import wx
import models
import views
import data
import datetime
from wx.lib.pubsub import Publisher as pub
import cPickle as pickle

from models import *
from views.MainFrame import MainFrame
from views.NuevoClienteFrame import NuevoClienteFrame
from views.DetalleClienteFrame import DetalleClienteFrame
from views.InformeTextoFrame import InformeTextoFrame
from views.InformeListaFrame import InformeListaFrame
from views.PrendaFrame import PrendaFrame

class AppController:
    """
    Controlador principal de la app.
    """

    def __init__(self, app):

        self.app = app
        self.data = data.load()

        self.clientes = self.data["clientes"]
        self.prendas = self.data["prendas"]
        self.configuracion = self.data["configuracion"]
        self.carrito = models.Carrito()

        self.main_window = MainFrame(None, -1, "A&M Moda")
        self.initUi()
        self.connectEvent()
        self.main_window.Show()

    def initUi(self):

        lista_clientes = self.main_window.lista_clientes

        # Agregar columnas a lista_clientes
        lista_clientes.InsertColumn(0, "DNI", width=100)
        lista_clientes.InsertColumn(1, "Nombre", width=300)
        lista_clientes.InsertColumn(2, "Telefono", width=200)
        lista_clientes.InsertColumn(3, "Saldo")# lista_clientes 


        # lista_prendas
        lista_prendas= self.main_window.lista_prendas

        # Agregar columnas a lista_clientes
        lista_prendas.InsertColumn(0, "Codigo", width=100)
        lista_prendas.InsertColumn(1, "Nombre", width=300)
        lista_prendas.InsertColumn(2, "Precio", width=200)  

        #setear menus con la configuracion
        self.main_window.ver_disponibles.Check(self.configuracion.mostrar_disponibles)
        self.main_window.ver_condicionales.Check(self.configuracion.mostrar_condicionales)
        self.main_window.ver_vendidas.Check(self.configuracion.mostrar_vendidas)
        self.main_window.ver_al_dia.Check(self.configuracion.mostrar_al_dia)
        self.main_window.ver_tardios.Check(self.configuracion.mostrar_tardios)
        self.main_window.ver_morosos.Check(self.configuracion.mostrar_morosos)



    def agregarClienteALista(self, item, indx=-1):

        lista_clientes = self.main_window.lista_clientes

        # Agregar items a lista_clientes
        idx = lista_clientes.GetItemCount()
        lista_clientes.InsertStringItem(idx, "%s" % item.getDni()) 
        lista_clientes.SetStringItem(idx, 1, "%s" % item.getNombre()) 
        lista_clientes.SetStringItem(idx, 2, "%s" % item.getTelefono()) 
        lista_clientes.SetStringItem(idx, 3, "%s" % item.getSaldo()) 

        if item.getEstado() == 'moroso':
            lista_clientes.SetItemBAckgroundColor(idx, "red")

        if item.getEstado() == 'tardio':
            lista_clientes.SetItemBAckgroundColor(idx, "yellow")


    def agregarPrendaALista(self, item, indx=-1):
        
        # Agregar items a lista_prendas
        idx = self.main_window.lista_prendas.GetItemCount()
        lista_prendas.InsertStringItem(idx, "%s" % item.getCodigo()) 
        lista_prendas.SetStringItem(idx, 1, "%s" % item.getNombre()) 
        lista_prendas.SetStringItem(idx, 2, "%s" % item.getPrecio()) 

        if item.getEstado() == 'vendida':
            lista_prendas.SetItemBAckgroundColor(idx, "red")

        if item.getEstado() == 'condicional':
            lista_prendas.SetItemBAckgroundColor(idx, "yellow")


    def agregarClientesActivos(self, clientes=[]):

        self.main_window.lista_clientes.DeleteAllItems()

        if len(clientes.getClientes()) > 0:
            cl = clientes
        else:
            cl = self.clientes.getClientesActivos(self.configuracion)

        for c in cl.getClientes():
            self.agregarClienteALista(c)


    def agregarPrendasActivas(self, prendas=[]):

        if len(prendas) > 0:
            pr = prendas
        else:
            pr = self.prendas.getPrendasActivas(self.configuracion)

        for p in pr:
            self.agregarClienteALista(p)

    def connectEvent(self):
        
        #vinculacion pestania prendas eventos
        self.main_window.boton_detalle_prendas.Bind(wx.EVT_BUTTON, self.mostrarDetallePrenda)
        self.main_window.boton_eliminar_prendas.Bind(wx.EVT_BUTTON, self.eliminarPrenda)
        self.main_window.boton_nuevo_prendas.Bind(wx.EVT_BUTTON, self.nuevaPrenda)
        self.main_window.boton_agregar_quitar.Bind(wx.EVT_BUTTON, self.agregarQuitarCarrito)
        self.main_window.boton_realizar_venta.Bind(wx.EVT_BUTTON, self.realizarVenta)

        self.main_window.texto_buscar_prendas.Bind(wx.EVT_SET_FOCUS, self.onSetFocusBuscarPrendas)
        self.main_window.texto_buscar_prendas.Bind(wx.EVT_KILL_FOCUS, self.onKillFocusBuscarPrendas)
        self.main_window.texto_buscar_prendas.Bind(wx.EVT_TEXT_ENTER, self.buscarPrendas)


        #viculacion pestania clientes eventos
        self.main_window.boton_detalle_clientes.Bind(wx.EVT_BUTTON, self.mostrarDetalleCliente)
        self.main_window.boton_eliminar_clientes.Bind(wx.EVT_BUTTON, self.eliminarCliente)
        self.main_window.boton_nuevo_clientes.Bind(wx.EVT_BUTTON, self.nuevoCliente)

        self.main_window.texto_buscar_clientes.Bind(wx.EVT_SET_FOCUS, self.onSetFocusBuscarClientes)
        self.main_window.texto_buscar_clientes.Bind(wx.EVT_KILL_FOCUS, self.onKillFocusBuscarClientes)
        self.main_window.texto_buscar_clientes.Bind(wx.EVT_TEXT_ENTER, self.buscarClientes)

        #vinculacion eventos menu

        self.main_window.Bind(wx.EVT_MENU, self.realizarBackup, self.main_window.realizar_backup)
        self.main_window.Bind(wx.EVT_MENU, self.restaurarBackup, self.main_window.restaurar_backup)
        self.main_window.Bind(wx.EVT_MENU, self.verDisponibles, self.main_window.ver_disponibles) 
        self.main_window.Bind(wx.EVT_MENU, self.verCondicionales, self.main_window.ver_condicionales)
        self.main_window.Bind(wx.EVT_MENU, self.verVendidas, self.main_window.ver_vendidas)
        self.main_window.Bind(wx.EVT_MENU, self.verAlDia, self.main_window.ver_al_dia)
        self.main_window.Bind(wx.EVT_MENU, self.verTardios, self.main_window.ver_tardios)
        self.main_window.Bind(wx.EVT_MENU, self.verMorosos, self.main_window.ver_morosos)
        self.main_window.Bind(wx.EVT_MENU, self.vaciarCarrito, self.main_window.vaciar_carrito)
        self.main_window.Bind(wx.EVT_MENU, self.listaCorreos, self.main_window.informe_lista_correos)
        self.main_window.Bind(wx.EVT_MENU, self.listaCorreosMorosos, self.main_window.informe_lista_correos_morosos)
        self.main_window.Bind(wx.EVT_MENU, self.listaTelefonos, self.main_window.informe_lista_telefonos)
        self.main_window.Bind(wx.EVT_MENU, self.listaTelefonosMorosos, self.main_window.informe_lista_telefonos_morosos)
        self.main_window.Bind(wx.EVT_MENU, self.listaCumpleaniosMes, self.main_window.informe_lista_cumpleanios_mes)
        self.main_window.Bind(wx.EVT_MENU, self.informeTotales, self.main_window.informe_totales)
        
        #suscripcion a eventos de Cliente
        pub.subscribe(self.clienteActualizado, "CAMBIO_CLIENTE")
        pub.subscribe(self.clienteActualizado, "COMPRA_AGREGADA")
        pub.subscribe(self.clienteActualizado, "PAGO_AGREGADO")
        pub.subscribe(self.clienteActualizado, "COMPRA_ELIMINADA")
        pub.subscribe(self.clienteActualizado, "PAGO_ELIMINADO")

        #suscripcion a eventos de Prenda
        pub.subscribe(self.prendaActualizada, "CAMBIO_PRENDA")

        #suscripcion a eventos de ListaClientes
        pub.subscribe(self.clienteAgregado, "CLIENTE_AGREGADO")
        pub.subscribe(self.clienteEliminado, "CLIENTE_ELIMINADO")

        #suscripcion a eventos de ListaPrendas
        pub.subscribe(self.prendaAgregada, "PRENDA_AGREGADA")
        pub.subscribe(self.prendaEliminada, "PRENDA_ELIMINADA")


        #suscripcion a eventos de Configuracion
        pub.subscribe(self.actualizadaConfiguracionPrendas, "CONFIGURACION_PRENDAS_CAMBIO")
        pub.subscribe(self.actualizadaConfiguracionClientes, "CONFIGURACION_CLIENTES_CAMBIO")

        #suscripcion a eventos carrito
        pub.subscribe(self.prendaAgregadaCarrito, "PRENDA_AGREGADA_CARRITO")
        pub.subscribe(self.prendaEliminadaCarrito, "PRENDA_ELIMINADA_CARRITO")
        pub.subscribe(self.carritoVaciado, "CARRITO_VACIADO")
        

    #metodos de la pestania prendas----------------------------------------------

        pub.subscribe(self.prendaAgregadaCarrito, "PRENDA_AGREGADA_CARRITO")
        pub.subscribe(self.prendaEliminadaCarrito, "PRENDA_ELIMINADA_CARRITO")
        pub.subscribe(self.carritoVaciado, "CARRITO_VACIADO")
        
    def mostrarDetallePrenda(self):

        seleccionado = self.main_window.lista_prendas.GetFocusedItem()
        
        if seleccionado != -1:
            codigo_prenda = self.main_window.lista_prendas.GetItem(seleccionado,0)
            prenda = self.prendas.getPrendaPorCodigo(int(codigo_prenda))
            controlador_detalle_prenda = DetallePrendaController(prenda, self.main_window)

    def eliminarPrenda(self, event):

        seleccionado = self.main_window.lista_prendas.GetFocusedItem()

        if seleccionado != -1:
            codigo_prenda = self.main_window.lista_prendas.GetItem(seleccionado,0)
            prenda = self.prendas.getPrendaPorCodigo(int(codigo_prenda))
            
            try:
                self.prendas.deletePrenda(prenda)
            except NameError:
                error_dialog = wx.MessageDialog(self.main_window, "No puede eliminar una prenda vendida o en condicional", "Advertencia", wx.ICON_INFORMATION)
                error_dialog.ShowModal()
                error_dialog.Destroy()
                self.Close()



    def nuevaPrenda(self, event):

        #recibe self para poder agregar la prenda a la lista prendas. Self.main_window es la ventana padre
        controlador_nueva_prenda = NuevaPrendaController(self.prendas, self.main_window)

    def agregarQuitarCarrito(self, event):
        
        seleccionado = self.main_window.lista_prendas.GetFocusedItem()

        if seleccionado != -1:
            item = self.main_window.lista_prendas.GetItem(seleccionado,0)
            codigo_prenda = item.GetText()
            prenda = self.prendas.getPrendaPorCodigo(int(codigo_prenda))
            
            try:
                carrito.addOrDeletePrenda(prenda)
            except NameError:
                error_dialog = wx.MessageDialog(self.main_window, "No puede vender una prenda vendida o en condicional", "Advertencia", wx.ICON_INFORMATION)
                error_dialog.ShowModal()
                error_dialog.Destroy()
                self.Close()

    def realizarVenta(self, event):
        if len(self.carrito.getPrendas()) != 0:
            controlador_venta = Venta_Controller(self.carrito, self.main_window)
        else:
            error_dialog = wx.MessageDialog(self.main_window, "Seleccione al menos una prenda para vender", "Advertencia", wx.ICON_INFORMATION)
            error_dialog.ShowModal()
            error_dialog.Destroy()
            self.Close()

    def onSetFocusBuscarPrendas(self, event):
        if self.main_window.texto_buscar_prendas.GetValue() == 'Buscar...':
            self.main_window.texto_buscar_prendas.Clear()


    def onKillFocusBuscarPrendas(self, event):
        if self.main_window.texto_buscar_prendas.GetValue() == '':
            self.main_window.texto_buscar_prendas.SetValue('Buscar...')

    def buscarPrendas(self, event):
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

        self.agregarPrendasActivas(lista_a_cargar)


    
    #metodos de la pestania clientes---------------------------------------------

    def mostrarDetalleCliente(self, event):

        seleccionado = self.main_window.lista_clientes.GetFocusedItem()
        
        if seleccionado != -1:
            item = self.main_window.lista_clientes.GetItem(seleccionado,0)
            dni = item.GetText()
            cliente = self.clientes.getClientePorDni(dni)
            controlador_detalle_cliente = DetalleClienteController(cliente, self.main_window)        

    def eliminarCliente(self, event):

        seleccionado = self.main_window.lista_clientes.GetFocusedItem()
        
        if seleccionado != -1:
            item = self.main_window.lista_clientes.GetItem(seleccionado,0)
            dni = item.GetText()
            cliente = self.clientes.getClientePorDni(dni)
            self.clientes.deleteCliente(cliente)
    
    def nuevoCliente(self, event):
        #recibe self para poder agregar la prenda a la lista clientes
        controlador_nuevo_cliente = NuevoClienteController(self.clientes, self.main_window)

    def onSetFocusBuscarClientes(self, event):
        if self.main_window.texto_buscar_clientes.GetValue() == 'Buscar...':
            self.main_window.texto_buscar_clientes.Clear()

    def onKillFocusBuscarClientes(self, event):
        if self.main_window.texto_buscar_clientes.GetValue() == '':
            self.main_window.texto_buscar_clientes.SetValue('Buscar...')

    def buscarClientes(self, event):

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

        self.agregarClientesActivos(lista_a_cargar)


    #metodos de suscripcion a eventos--------------------------------------------
    def clienteActualizado(self, message):
        
        self.agregarClientesActivos()

    def prendaActualizada(self, message):
    
        for idx in range(self.main_window.lista_prendas.GetItemCount()): 
            item = self.main_window.lista_prendas.GetItem(idx, 0) 
            if item.GetText() == message.data.getDni():
                self.main_window.lista_prendas.DeleteItem(item)
                self.agregarPrendaALista(message.data, idx)
                break

    def clienteAgregado(self, message):

        self.agregarClienteALista(message.data)

    def clienteEliminado(self, message):

        self.agregarClientesActivos()

    def prendaAgregada(self, message):
        
        self.agregarPrendaALista(message.data)

    def prendaEliminada(self, message):
    
        for idx in range(self.main_window.lista_prendas.GetItemCount()): 
            item = self.main_window.lista_prendas.GetItem(idx, 0) 
            if item.GetText() == message.data.getDni():
                self.main_window.lista_prendas.DeleteItem(item)
                break


    def actualizadaConfiguracionPrendas(self, message):
        self.agregarPrendasActivas()

    def actualizadaConfiguracionClientes(self, message):
        self.agregarClientesActivos()

    def prendaAgregadaCarrito(self, message):
        
        seleccionado = self.main_window.lista_prendas.GetFocusedItem()

        if seleccionado != -1:
            self.main_window.lista_prendas.SetItemBackgroundColor(seleccionado, "green")    

    def prendaEliminadaCarrito(self, message):
        seleccionado = self.main_window.lista_prendas.GetFocusedItem()

        if seleccionado != -1:
            self.main_window.lista_prendas.SetItemBackgroundColor(seleccionado, "white")

    def carritoVaciado(self, message):
        self.agregarPrendasActivas()

    #metodos barra menu------------------------------------------------------------

    def realizarBackup(self, event):
        
        # Abrir dialogo para seleccionar ruta de destino del archivo de backup
        file_dialog = wx.FileDialog(self.main_window, style = wx.SAVE)
        d = datetime.date.today()
        filename = "%s-%s-%s-backup.bak" % (d.day, d.month, d.year)
        file_dialog.SetFilename(filename)
        file_dialog.SetWildcard("Archivos de Backup (*.bak)|*.bak|Todos los archivos (*.*)|*.*")
        if file_dialog.ShowModal() == wx.ID_OK:
                data.backup(file_dialog.GetPath())
                msgbox = wx.MessageDialog(self.main_window, "Archivo de backup creado satisfactoriamente.", "INFO", style=wx.ICON_INFORMATION)
                msgbox.ShowModal()

    def restaurarBackup(self, event):
        #leo copia del sgpd vos que entendes tu codigo jaja
        pass
    
    def verDisponibles(self, event):
        self.configuracion.setMostrarDisponibles(self.main_window.ver_disponibles.IsChecked())        

    def verCondicionales(self, event):
        self.configuracion.setMostrarCondicionales(self.main_window.ver_condicionales.IsChecked())

    def verVendidas(self, event):
        self.configuracion.setMostrarVendidas(self.main_window.ver_vendidas.IsChecked())

    def verAlDia(self, event):
        self.configuracion.setMostrarAlDia(self.main_window.ver_al_dia.IsChecked())

    def verTardios(self, event):
        self.configuracion.setMostrarTardios(self.main_window.ver_tardios.IsChecked())

    def verMorosos(self, event):
        self.configuracion.setMostrarMorosos(self.main_window.ver_morosos.IsChecked())    
    
    def vaciarCarrito(self, event):
        self.carrito.vaciarCarrito()

    def listaCorreos(self, event):
        correos = ''

        for cliente in self.clientes.getClientes():
            correos = correos + cliente.getEmail() + ';'

        controlador_infome = InformeTextoController('E-mail Clientes', correos, self.main_window)

    def listaCorreosMorosos(self, event):
        correos = ''

        for cliente in self.clientes.getClientesMorosos():
            correos = correos + cliente.getEmail() + ';'

        controlador_infome = InformeTextoController('E-mail Clientes Morosos', correos, self.main_window)

    def listaTelefonos(self, event):

        columnas = ['DNI', 'Nombre', 'Telefono']
        telefonos= []

        for cliente in self.clientes.getClientes():
            tupla_datos = (cliente.getDni(), cliente.getNombre(), cliente.getTelefono())

            telefonos.append(tupla_datos)

        controlador_infome = InformeListaController('Lista de Telefonos', columnas, telefonos, self.main_window)

    def listaTelefonosMorosos(self, event):
        
        columnas = ['DNI', 'Nombre', 'Telefono']
        telefonos= []

        for cliente in self.clientes.getClientesMorosos():
            tupla_datos = (cliente.getDni(), cliente.getNombre(), cliente.getTelefono())

            telefonos.append(tupla_datos)

        controlador_infome = InformeListaController('Lista de Telefonos Morosos', columnas, telefonos, self.main_window)      

    def listaCumpleaniosMes(self, event):

        columnas = ['DNI', 'Nombre', 'Telefono', 'E-mail']
        cumpleanieros = []

        for cliente in self.clientes.getClientes():
            if cliente.cumpleAniosEsteMes():
                tupla_datos = (cliente.getDni(), cliente.getNombre(), cliente.getTelefono(), cliente.getEmail())
                cumpleanieros.append(tupla_datos)
        
        controlador_infome = InformeListaController('Lista Cumpleanos', columnas, cumpleanieros, self.main_window)


    def informeTotales(self, event):
        total_ganancias = 0
        total_deuda = 0
        total_capital_en_prendas = 0
        total_inversion = 0


        for prenda in self.prendas.getPrendas():
            
            total_inversion += prenda.precio

            if prenda.getEstado() == 'vendida':
                total_ganancias += (prenda.precio - prenda.costo)

            if (prenda.getEstado() == 'disponible') or (prenda.getEstado() == 'condicional'):
                total_capital_en_prendas += prenda.precio

        for cliente in self.clientes.getClientes():

            total_deuda += cliente.getSaldo()

        columnas = ['Indicador', 'Total']
        totales = []
        totales.append(('Total Ganancias', total_ganancias))
        totales.append(('Total Deudas', total_deuda))
        totales.append(('Total Inversion', total_inversion))
        totales.append(('Capital en Stock', total_capital_en_prendas))

        controlador = InformeListaController('Informe de Totales', columnas, totales, self.main_window)

        #se debe instanciar la ventana que tiene los totales


class DetalleClienteController:
    """
    COntrolador Detalle Cliente
    """

    def __init__(self, cliente, padre):

        self.cliente = cliente
        self.detalle_window = DetalleClienteFrame(padre, -1, "Detalle Cliente %s" %cliente.getNombre())
        self.detalle_window.Centre()
        self.initUi()
        self.connectEvent()
        self.detalle_window.Show()

    def initUi(self):


        # lista_resumen_clientes    
        list_resumen_cliente = self.detalle_window.list_resumen_cliente

        # Agregar columnas a lista_resumen_cliente
        list_resumen_cliente.InsertColumn(0, "Fecha", width=90)
        list_resumen_cliente.InsertColumn(1, "Tipo", width=100)
        list_resumen_cliente.InsertColumn(2, "Codigo", width=100)
        list_resumen_cliente.InsertColumn(3, "Nombre", width=150)
        list_resumen_cliente.InsertColumn(4, "Monto", width=80)

        #Agregar los movimientos a la lista
        self.agregarMovimientos()

        #setear datos del cliente
        self.detalle_window.texto_dni.SetLabel(self.cliente.getDni())
        self.detalle_window.texto_nombre.SetValue(self.cliente.getNombre())
        self.detalle_window.texto_direccion.SetValue(self.cliente.getDireccion())
        self.detalle_window.date_fecha_nacimiento.SetValue(self.cliente.getFechaNacimiento())
        self.detalle_window.texto_telefono.SetValue(self.cliente.getTelefono())
        self.detalle_window.text_email.SetValue(self.cliente.getEmail())

        #deshabilita inicialmente el boton guardar
        self.disableGuardar()

        #setear si el cliente debe o tiene credito
        if self.cliente.getSaldo() < 0:
            self.detalle_window.label_saldo.SetValue("Credito")
            self.detalle_window.label_saldo_imagen.SetValue(self.cliente.getSaldo()*(-1))
        else:
            self.detalle_window.label_saldo_imagen.SetLabel(str(self.cliente.getSaldo()))


    def connectEvent(self):

        #botones
        self.detalle_window.boton_eliminar_accion.Bind(wx.EVT_BUTTON, self.eliminarAccion)
        self.detalle_window.boton_eliminar_condicional.Bind(wx.EVT_BUTTON, self.eliminarCondicionales)
        self.detalle_window.boton_guardar.Bind(wx.EVT_BUTTON, self.guardar)
        self.detalle_window.boton_cerrar.Bind(wx.EVT_BUTTON, self.cerrar)

        #textos
        self.detalle_window.texto_paga_con.Bind(wx.EVT_TEXT_ENTER, self.calcularVuelto)

        self.detalle_window.texto_nombre.Bind(wx.EVT_TEXT, self.enableGuardar)
        self.detalle_window.texto_direccion.Bind(wx.EVT_TEXT, self.enableGuardar)

        self.detalle_window.texto_telefono.Bind(wx.EVT_TEXT, self.enableGuardar)
        self.detalle_window.text_email.Bind(wx.EVT_TEXT, self.enableGuardar)

        #calendario
        self.detalle_window.date_fecha_nacimiento.Bind(wx.EVT_DATE_CHANGED, self.enableGuardar)

        #suscripcion a eventos
        pub.subscribe(self.accionEliminada, "COMPRA_ELIMINADA")
        pub.subscribe(self.accionEliminada, "PAGO_ELIMINADO")
        pub.subscribe(self.accionEliminada, "PAGO_AGREGADO")
        pub.subscribe(self.accionEliminada, "CONDICIONALES_ELIMINADOS")
    
    def agregarMovimientoALista(self, movimiento):
        idx = self.detalle_window.list_resumen_cliente.GetItemCount()
        list_resumen_cliente = self.detalle_window.list_resumen_cliente
        
        if isinstance(movimiento, Compra):
            list_resumen_cliente.InsertStringItem(idx, "%s" % movimiento.fecha)
            list_resumen_cliente.SetStringItem(idx, 1, "Compra")
            list_resumen_cliente.SetStringItem(idx, 2, "%s" % movimiento.prenda.getCodigo())
            list_resumen_cliente.SetStringItem(idx, 3, "%s" % movimiento.prenda.getNombre())
            list_resumen_cliente.SetStringItem(idx, 4, "%s" % movimiento.monto)                
        elif isinstance(movimiento, Pago):
            list_resumen_cliente.InsertStringItem(idx, "%s" % movimiento.fecha)
            list_resumen_cliente.SetStringItem(idx, 1, "Pago") 
            list_resumen_cliente.SetStringItem(idx, 2, "-")
            list_resumen_cliente.SetStringItem(idx, 3, "-") 
            list_resumen_cliente.SetStringItem(idx, 4, "%s" % movimiento.monto)
        elif isinstance(movimiento, Condicional):
            list_resumen_cliente.InsertStringItem(idx, "%s" % movimiento.fecha)
            list_resumen_cliente.SetStringItem(idx, 1, "Condicional") 
            list_resumen_cliente.SetStringItem(idx, 2, "%s" % movimiento.prenda.getCodigo())
            list_resumen_cliente.SetStringItem(idx, 3, "%s" % movimiento.prenda.getNombre())
            list_resumen_cliente.SetStringItem(idx, 4, "0")

    def agregarMovimientos(self):

        for mov in self.cliente.getMovimientos():
            self.agregarMovimientoALista(mov)

    def eliminarAccion(self, event):
        #como los mov no tienen un "id" voy a eliminarlos con la posicon de la tabla
        seleccionado = self.detalle_window.list_resumen_cliente.GetFocusedItem()
        
        if seleccionado != -1:
            movimiento = cliente.getMovimientos()[seleccionado]
            if isinstance(movimiento, 'Compra'):
                cliente.deleteCompra(movimiento)
            elif isinstance(movimiento, 'Pago'):
                cliente.deletePago(movimiento)
            elif isinstance(movimiento, 'Condicional'):
                cliente.deleteCondicional(movimiento)

    def eliminarCondicionales(self, event):
        
        cliente.deleteCondicionales()

    def guardar(self, event):

        self.cliente.setNombre(self.detalle_window.texto_nombre.GetValue())
        self.cliente.setTelefono(self.detalle_window.texto_telefono.GetValue())
        self.cliente.setEmail(self.detalle_window.text_email.GetValue())
        self.cliente.setFechaNacimiento(self.detalle_window.date_fecha_nacimiento.GetValue())
        self.cliente.setDireccion(self.detalle_window.texto_direccion.GetValue())

        #una vez guardado deshabilitamos el boton guardar
        self.disableGuardar()

    def cerrar(self, event):
        self.detalle_window.Destroy()
        #hay que destruir el objeto o la ventana

    def calcularVuelto(self, event):

        entrega = float(self.detalle_window.texto_entrega.GetValue())
        paga_con = float(self.detalle_window.texto_paga_con.GetValue())
        
        if entrega <= paga_con:
            self.detalle_window.label_vuelto_imagen.SetLabel(str(paga_con - entrega))
            new_pago = Pago(entrega, self.cliente)
            self.cliente.addPago(new_pago)
            self.detalle_window.label_saldo_imagen.SetLabel(str(self.cliente.getSaldo()))
        else:
            error_dialog = wx.MessageDialog(self.detalle_window, "No puede pagar con menos de lo que entrega", "Advertencia", wx.ICON_INFORMATION)
            error_dialog.ShowModal()
            error_dialog.Destroy()
            self.Close()

    def accionEliminada(self, message):
        #recargamos movimientos del cliente
        self.agregarMovimientos()

    def enableGuardar(self, event):
        self.detalle_window.boton_guardar.Enable(True)

    def disableGuardar(self):
        self.detalle_window.boton_guardar.Enable(False)

class NuevoClienteController():


    def __init__(self, clientes, padre):

        self.clientes = clientes
        self.nuevo_window = NuevoClienteFrame(padre, -1, "Nuevo Cliente")
        self.nuevo_window.Centre()

        self.disableGuardar()
        self.connectEvent()

        self.nuevo_window.Show()


    def connectEvent(self):
        
        self.nuevo_window.boton_guardar.Bind(wx.EVT_BUTTON, self.guardar)
        self.nuevo_window.boton_cancelar.Bind(wx.EVT_BUTTON, self.cancelar)

        self.nuevo_window.texto_dni.Bind(wx.EVT_TEXT, self.enableGuardar)

    def guardar(self, event):
        dni = self.nuevo_window.texto_dni.GetValue()
        nombre = self.nuevo_window.texto_nombre.GetValue()
        telefono = self.nuevo_window.texto_telefono.GetValue()
        email = self.nuevo_window.text_email.GetValue()
        fecha_nacimiento = self.nuevo_window.date_fecha_nacimiento.GetValue()
        direccion = self.nuevo_window.texto_direccion.GetValue()
        
        new_cliente = Cliente(dni, nombre, telefono, email, direccion, fecha_nacimiento)
        try:
            self.clientes.addCliente(new_cliente)
        except NameError:
            error_dialog = wx.MessageDialog(self.nuevo_window, "Ya existe un cliente con ese DNI", "Advertencia", wx.ICON_INFORMATION)
            error_dialog.ShowModal()
            error_dialog.Destroy()
            self.Close()


        #hay que cerrar la ventana o destruir el objeto

    def cancelar(self, event):
        #hay que cerrar la ventana o destruir el objeto
        pass
    

    def enableGuardar(self, event):
        if (len(self.nuevo_window.texto_dni.GetValue()) == 8):
            self.nuevo_window.boton_guardar.Enable(True)
        else:
            self.disableGuardar()

    def disableGuardar(self):
        self.nuevo_window.boton_guardar.Enable(False)

class InformeTextoController:
    """
    Controlador de Informe de Texto
    """

    def __init__(self, titulo, correos, padre):

        self.titulo = titulo
        self.correos = correos
        self.informe_window = InformeTextoFrame(padre, -1, "Informe")
        

        self.informe_window.text_titulo.SetValue(correos)
        self.informe_window.label_titulo.SetLabel(titulo)
        self.informe_window.Show()


class InformeListaController:
    """
    Controlador de Informe Lista
    """

    def __init__(self, titulo, columnas, telefonos, padre):

        self.titulo = titulo
        self.columnas = columnas
        self.telefonos = telefonos
        self.informe_window = InformeListaFrame(padre, -1, "Informe")
        self.initUi()
        
        self.informe_window.Show()
        self.informe_window.label_titulo.SetLabel(titulo)

    def initUi(self):


        # lista_telefonos   
        list_titulo = self.informe_window.list_titulo

        # Agregar columnas a lista_telefonos
        j = 0
        for i in self.columnas:
            list_titulo.InsertColumn(j, i, width=150)
            j = j + 1

        #Agregar los movimientos a la lista
        for i in self.telefonos:
            idx = list_titulo.GetItemCount()
            cont = 0
            for elem in i:
                if (cont == 0):
                    list_titulo.InsertStringItem(idx, "%s" % elem)
                else:
                    list_titulo.SetStringItem(idx, cont, "%s" % elem)
                cont = cont + 1


class NuevaPrendaController:
    """
    Controlador de nueva prenda
    """

    def __init__(self, prendas, padre):

        self.prendas = prendas
        self.nueva_window = PrendaFrame(padre, -1, "Nueva Prenda")
        self.nueva_window.Centre()

        self.disableGuardar()
        self.connectEvent()

        self.nueva_window.Show()

    def connectEvent(self):
        
        self.nueva_window.boton_guardar.Bind(wx.EVT_BUTTON, self.guardar)
        self.nueva_window.boton_cancelar.Bind(wx.EVT_BUTTON, self.cancelar)

        self.nueva_window.texto_nombre.Bind(wx.EVT_TEXT, self.enableGuardar)
        self.nueva_window.texto_costo.Bind(wx.EVT_TEXT, self.enableGuardar)
        self.nueva_window.texto_precio.Bind(wx.EVT_TEXT, self.enableGuardar)

    def guardar(self, event):

        nombre = self.nueva_window.texto_nombre.GetValue()
        talle = self.nueva_window.texto_talle.GetValue()
        costo = float(self.nueva_window.texto_costo.GetValue())
        precio = float(self.nueva_window.texto_precio.GetValue())
        descripcion = self.nueva_window.text_descripcion.GetValue()

        new_prenda = Prenda(nombre, talle, costo, precio, descripcion)

        self.prendas.addPrenda(new_prenda)

        vendida = self.nueva_window.combo_box_vendida.GetValue()

        if vendida == "Si":
            new_prenda.setCliente(cliente_casual)
            new_compra = Compra(new_prenda.getPrecio(), new_prenda, cliente_casual)
            cliente_casual.addCompra(new_compra)

        msgbox = wx.MessageDialog(self.nueva_window, "El codigo de la nueva prenda es %s" %new_prenda.getCodigo(), "Informacion", style=wx.ICON_INFORMATION)
        msgbox.ShowModal()

    def cancelar(self, event):
        pass


    def enableGuardar(self, event):
        if ((self.nueva_window.texto_nombre.GetValue()) != "") and ((self.nueva_window.texto_costo.GetValue()) != "") and ((self.nueva_window.texto_precio.GetValue()) != ""):
            self.nueva_window.boton_guardar.Enable(True)
        else:
            self.disableGuardar()

    def disableGuardar(self):
        self.nueva_window.boton_guardar.Enable(False)       


class DetallePrendaController:
    """
    Controlador detalle prenda
    """

    def __init__(self, prenda, padre):

        self.prenda = prendas
        self.detalle_window = PrendaFrame(padre, -1, "Detalle Prenda %s" %prenda.getCodigo())
        self.detalle_window.Centre()
        self.initUi()

        self.disableGuardar()
        self.connectEvent()

        self.detalle_window.Show()

    def initui(self):
        self.detalle_window.texto_nombre.SetValue(self.prenda.getNombre())
        self.detalle_window.texto_talle.SetValue(self.prenda.getTalle())
        self.detalle_window.texto_costo.SetValue(self.prenda.getCosto())
        self.detalle_window.texto_precio.SetValue(self.prenda.getPrecio())
        self.detalle_window.text_descripcion.SetValue(self.prenda.getDescripcion())

        if self.prenda.getEstado == 'vendida':
            self.detalle_window.combo_box_vendida.SetValue('Si')

    def connectEvent(self):
        
        self.detalle_window.boton_guardar.Bind(wx.EVT_BUTTON, self.guardar)
        self.detalle_window.boton_cancelar.Bind(wx.EVT_BUTTON, self.cancelar)

        self.detalle_window.texto_nombre.Bind(wx.EVT_TEXT, self.enableGuardar)
        self.detalle_window.texto_costo.Bind(wx.EVT_TEXT, self.enableGuardar)
        self.detalle_window.texto_precio.Bind(wx.EVT_TEXT, self.enableGuardar)
        self.detalle_window.texto_talle.Bind(wx.EVT_TEXT, self.enableGuardar)
        self.detalle_window.text_descripcion.Bind(wx.EVT_TEXT, self.enableGuardar)
        self.detalle_window.combo_box_vendida.Bind(wx.EVT.COMBOBOX, self.enableGuardar)


    def guardar(self, event):

        self.prenda.setNombre(self.detalle_window.texto_nombre.GetValue())
        self.prenda.setTalle(self.detalle_window.texto_talle.GetValue())
        self.prenda.setCosto(float(self.detalle_window.texto_costo.GetValue()))
        self.prenda.setPrecio(float(self.detalle_window.texto_precio.GetValue()))
        self.prenda.setDescripcion(self.detalle_window.text_descripcion.GetValue())

        vendida = self.detalle_window.combo_box_vendida.GetValue()

        if vendida == "Si" and self.prenda.getEstado() == "disponble":
            new_prenda.setCliente(cliente_casual)
            new_compra = Compra(new_prenda.getPrecio(), new_prenda, cliente_casual)
            cliente_casual.addCompra(new_compra)
        elif vendida == "Si" and self.prenda.getEstado() == "condicional":
                error_dialog = wx.MessageDialog(self.detalle_window, "Esta prenda esta en condicional, no puede marcarla como vendida", "Advertencia", wx.ICON_INFORMATION)
                error_dialog.ShowModal()
        elif vendida == "No" and self.prenda.getEstado() == "vendida"
            cliente = self.prenda.getCliente()
            compra = cliente.getCompraPorPrenda(self.prenda)
            cliente.deleteCompra(compra)
            self.prenda.setCliente(None)

    def cancelar(self, event):
        pass


    def enableGuardar(self, event):
        if ((self.detalle_window.texto_nombre.GetValue()) != "") and ((self.detalle_window.texto_costo.GetValue()) != "") and ((self.detalle_window.texto_precio.GetValue()) != ""):
            self.detalle_window.boton_guardar.Enable(True)
        else:
            self.disableGuardar()

    def disableGuardar(self):
        self.detalle_window.boton_guardar.Enable(False)            


if __name__=='__main__':
    
    app = wx.App(False)
    controller = AppController(app)
    app.MainLoop()

