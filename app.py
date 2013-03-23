import wx
import models
import views
from wx.lib.pubsub import Publisher as pub

class AppController:
    """
    Controlador principal de la app.
    """

    def __init__(self, app):

        self.app = app

	self.initUi()
	self.connectEvents()


    def initUi(self):

        pass


    def connectEvents(self):
        
	pass


if __name__=='__main__':
    
    app = wx.App(False)
    controller = AppController(app)
    app.MainLoop()

