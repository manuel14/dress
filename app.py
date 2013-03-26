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
	
        


if __name__=='__main__':
    
    app = wx.App(False)
    controller = AppController(app)
    app.MainLoop()

