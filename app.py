#!pythonw

'''
Bob Miller Book Room ordering application

author: Simon Malcolm
'''
import wx

class OrderApp(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(OrderApp, self).__init__(*args, **kwargs)

        self.InitUI()

    def InitUI(self):
        menubar = wx.MenuBar()

        fileMenu = wx.Menu()
        
        qmi = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+W')
        fileMenu.AppendItem(qmi)

        self.Bind(wx.EVT_MENU, self.OnQuit, qmi)

        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        self.SetSize((0, 0))
        self.SetTitle('Orders')
        self.Centre()
        self.Show(False)

    def OnQuit(self, e):
        self.Close()

def main():
    app = wx.App()
    OrderApp(None)
    app.MainLoop()

if __name__ == '__main__':
    main()
