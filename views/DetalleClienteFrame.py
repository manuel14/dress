#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.5 (standalone edition) on Sat Mar 23 17:51:32 2013

import wx

# begin wxGlade: extracode
# end wxGlade


class FrameDetalleCliente(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: FrameDetalleCliente.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.panel_1 = wx.Panel(self, -1)
        self.label_cliente = wx.StaticText(self.panel_1, -1, "CLIENTE")
        self.label_dni = wx.StaticText(self.panel_1, -1, "DNI")
        self.texto_dni = wx.TextCtrl(self.panel_1, -1, "")
        self.label_nombre = wx.StaticText(self.panel_1, -1, "Nombre")
        self.texto_nombre = wx.TextCtrl(self.panel_1, -1, "")
        self.label_direccion = wx.StaticText(self.panel_1, -1, u"Direcci�n")
        self.texto_direccion = wx.TextCtrl(self.panel_1, -1, "")
        self.label_telefono = wx.StaticText(self.panel_1, -1, "Telefono")
        self.texto_telefono = wx.TextCtrl(self.panel_1, -1, "")
        self.label_e-mail = wx.StaticText(self.panel_1, -1, "e-mail   ")
        self.texto_e-mail = wx.TextCtrl(self.panel_1, -1, "")
        self.panel_2 = wx.Panel(self, -1)
        self.static_line_1 = wx.StaticLine(self.panel_2, -1, style=wx.LI_VERTICAL)
        self.label_resumen_cuenta = wx.StaticText(self.panel_2, -1, "Resumen Cuenta")
        self.list_resumen_cliente = wx.ListCtrl(self.panel_2, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.boton_eliminar_accion = wx.Button(self.panel_2, -1, u"Eliminar\nAcci�n")
        self.boton_eliminar_condicional = wx.Button(self.panel_2, -1, "Eliminar\nCondicional")
        self.label_saldo = wx.StaticText(self.panel_2, -1, "Saldo")
        self.label_saldo_imagen = wx.StaticText(self.panel_2, -1, "")
        self.label_entrega = wx.StaticText(self.panel_2, -1, "Entrega")
        self.texto_entrega = wx.TextCtrl(self.panel_2, -1, "")
        self.label_paga_con = wx.StaticText(self.panel_2, -1, "Paga con")
        self.texto_paga_con = wx.TextCtrl(self.panel_2, -1, "")
        self.label_vuelto = wx.StaticText(self.panel_2, -1, "Vuelto")
        self.label_vuelto_imagen = wx.StaticText(self.panel_2, -1, "")
        self.boton_cancelar = wx.Button(self.panel_2, -1, "Cancelar")
        self.boton_aceptar = wx.Button(self.panel_2, -1, "Aceptar")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: FrameDetalleCliente.__set_properties
        self.SetTitle("frame_1")
        self.label_cliente.SetFont(wx.Font(25, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.label_dni.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.texto_dni.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.label_nombre.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.texto_nombre.SetMinSize((200, 31))
        self.texto_nombre.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.label_direccion.SetMinSize((65, 19))
        self.label_direccion.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.texto_direccion.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.label_telefono.SetMinSize((62, 19))
        self.label_telefono.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.texto_telefono.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.label_e-mail.SetMinSize((59, 19))
        self.label_e-mail.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.texto_e-mail.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.label_resumen_cuenta.SetFont(wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.list_resumen_cliente.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.boton_eliminar_accion.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.boton_eliminar_condicional.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.label_saldo.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_saldo_imagen.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.label_entrega.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.texto_entrega.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.label_paga_con.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.texto_paga_con.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.label_vuelto.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.label_vuelto_imagen.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: FrameDetalleCliente.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_1_copy = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_7 = wx.FlexGridSizer(1, 2, 0, 0)
        grid_sizer_6 = wx.FlexGridSizer(1, 6, 0, 0)
        grid_sizer_1 = wx.FlexGridSizer(1, 2, 0, 0)
        grid_sizer_4 = wx.FlexGridSizer(1, 2, 0, 0)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_3_copy_1 = wx.FlexGridSizer(1, 2, 0, 0)
        grid_sizer_3_copy = wx.FlexGridSizer(1, 2, 0, 0)
        grid_sizer_3 = wx.FlexGridSizer(1, 2, 0, 0)
        grid_sizer_2 = wx.FlexGridSizer(1, 5, 0, 0)
        sizer_4.Add(self.label_cliente, 0, wx.LEFT, 7)
        grid_sizer_2.Add(self.label_dni, 0, wx.LEFT | wx.TOP, 10)
        grid_sizer_2.Add(self.texto_dni, 0, wx.LEFT | wx.TOP, 8)
        grid_sizer_2.Add(self.label_nombre, 0, wx.LEFT | wx.TOP, 10)
        grid_sizer_2.Add(self.texto_nombre, 0, wx.LEFT | wx.TOP, 8)
        grid_sizer_2.AddGrowableCol(3)
        sizer_4.Add(grid_sizer_2, 1, wx.EXPAND, 0)
        grid_sizer_3.Add(self.label_direccion, 0, wx.LEFT | wx.TOP, 10)
        grid_sizer_3.Add(self.texto_direccion, 0, wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, 8)
        grid_sizer_3.AddGrowableCol(1)
        sizer_4.Add(grid_sizer_3, 1, wx.EXPAND, 0)
        grid_sizer_3_copy.Add(self.label_telefono, 0, wx.LEFT | wx.TOP, 10)
        grid_sizer_3_copy.Add(self.texto_telefono, 0, wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, 8)
        grid_sizer_3_copy.AddGrowableCol(1)
        sizer_4.Add(grid_sizer_3_copy, 1, wx.EXPAND, 0)
        grid_sizer_3_copy_1.Add(self.label_e-mail, 0, wx.LEFT | wx.TOP, 10)
        grid_sizer_3_copy_1.Add(self.texto_e-mail, 0, wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, 9)
        grid_sizer_3_copy_1.AddGrowableCol(1)
        sizer_4.Add(grid_sizer_3_copy_1, 1, wx.EXPAND, 0)
        self.panel_1.SetSizer(sizer_4)
        sizer_2.Add(self.panel_1, 1, wx.EXPAND, 0)
        sizer_5.Add(self.static_line_1, 0, wx.EXPAND, 0)
        sizer_5.Add(self.label_resumen_cuenta, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        grid_sizer_4.Add(self.list_resumen_cliente, 1, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 6)
        sizer_6.Add(self.boton_eliminar_accion, 0, wx.ALL, 5)
        sizer_6.Add(self.boton_eliminar_condicional, 0, wx.ALL, 5)
        grid_sizer_4.Add(sizer_6, 1, wx.EXPAND, 0)
        grid_sizer_4.AddGrowableCol(0)
        sizer_5.Add(grid_sizer_4, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.label_saldo, 0, wx.LEFT | wx.RIGHT | wx.TOP, 5)
        grid_sizer_1.Add(self.label_saldo_imagen, 0, wx.TOP, 5)
        sizer_1_copy.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        grid_sizer_6.Add(self.label_entrega, 0, wx.ALL, 4)
        grid_sizer_6.Add(self.texto_entrega, 0, wx.RIGHT | wx.TOP | wx.BOTTOM, 3)
        grid_sizer_6.Add(self.label_paga_con, 0, wx.ALL, 4)
        grid_sizer_6.Add(self.texto_paga_con, 0, wx.RIGHT | wx.TOP | wx.BOTTOM, 3)
        grid_sizer_6.Add(self.label_vuelto, 0, wx.ALL, 4)
        grid_sizer_6.Add(self.label_vuelto_imagen, 0, wx.ALL, 4)
        sizer_1_copy.Add(grid_sizer_6, 1, wx.EXPAND, 0)
        grid_sizer_7.Add(self.boton_cancelar, 0, wx.ALL | wx.ALIGN_RIGHT, 4)
        grid_sizer_7.Add(self.boton_aceptar, 0, wx.ALL, 4)
        grid_sizer_7.AddGrowableCol(0)
        sizer_1_copy.Add(grid_sizer_7, 1, wx.EXPAND, 0)
        sizer_5.Add(sizer_1_copy, 1, wx.EXPAND, 0)
        self.panel_2.SetSizer(sizer_5)
        sizer_2.Add(self.panel_2, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

# end of class FrameDetalleCliente
if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = FrameDetalleCliente(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
