#!pythonw

'''
Bob Miller Book Room ordering application

author: Simon Malcolm
'''
import wx

class MainWindow(wx.Frame):

    def __init__(self, title = "Order App"):
        wx.Frame.__init__(self, None, -1, title)

        self.InitUI()

    def InitUI(self):
        menubar = wx.MenuBar()

        fileMenu = wx.Menu()

        item = fileMenu.Append(wx.ID_ANY, 'Edit Book')
        
        item = fileMenu.Append(wx.ID_PREFERENCES, "&Preferences")
        self.Bind(wx.EVT_MENU, self.OnPrefs, item)
                
        item = fileMenu.Append(wx.ID_EXIT, '&Quit\tCtrl+W')
        self.Bind(wx.EVT_MENU, self.OnQuit, item)

        menubar.Append(fileMenu, "&File")

        helpMenu = wx.Menu()

        item = helpMenu.Append(wx.ID_HELP, "Test &Help",
                                "Help for this simple test")
        self.Bind(wx.EVT_MENU, self.OnHelp, item)

        item = helpMenu.Append(wx.ID_ABOUT, "&About",
                                "More information About this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, item)

        menubar.Append(helpMenu, "&Help")

        self.SetMenuBar(menubar)

        btn = wx.Button(self, label = "Quit")
        btn.Bind(wx.EVT_BUTTON, self.OnQuit)

        self.Bind(wx.EVT_CLOSE, self.OnQuit)

    def OnQuit(self, event):
        self.Destroy()

    def EditBook(self, event):
        BookEdit(None)

    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, "Bob Miller Book Room Orders",
                               "About Me", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnHelp(self, event):
        dlg = wx.MessageDialog(self, "This would be help\n"
                                     "If there was any\n",
                               "Help", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnPrefs(self, event):
        dlg = wx.MessageDialog(self, "Set Preferences here, eventually",
                               "Preferences", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

class OrderApp(wx.App):

    def __init__(self, *args, **kwargs):
        wx.App.__init__(self, *args, **kwargs)

        self.Bind(wx.EVT_ACTIVATE_APP, self.OnActivate)

    def OnInit(self):
        frame = MainWindow()
        frame.Show()

        return True

    def BringWindowToFront(self):
        try:
            self.GetTopWindow.Raise()
        except:
            pass

    def OnActivate(self, event):
        if event.GetActive():
            self.BringWindowToFront()
        event.Skip()

    def MacOpenFile(sel, filename):
        """Called for files dropped on dock icon or opened with context menu"""
        pass

    def MacReopenApp(self):
        """Called when the dock icon is clicked, maybe other times?"""
        self.BringWindowToFront()

    def MacNewFile(self):
        pass

    def MacPrintFile(self, file_path):
        pass

class BookEdit(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(BookEdit, self).__init__(*args, **kwargs)

        self.InitUI()

    def InitUI(self):
        self.SetSize((350, 250))
        self.SetTitle('Edit Book')
        self.Centre()

if __name__ == "__main__":
    app = OrderApp(False)
    app.MainLoop()
