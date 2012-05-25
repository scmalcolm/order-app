'''
Bob Miller Book Room ordering application

Copyright Simon Malcolm 2012
'''
import wx
from wx import xrc
import layout

class MainWindow(layout.MainFrame):

    def __init__(self, parent):
        layout.MainFrame.__init__(self, parent)
        wx.MenuBar.MacSetCommonMenuBar(self.menubar)
        
    def OnClose(self, event):
        if event.CanVeto():
            event.Veto()
        else:
            self.Destroy()
            event.Skip()

    def OnQuit(self, event):
        self.Close(force = True)

    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, "Bob Miller Book Room Orders\n"
                               "Application created by Simon Malcolm",
                               "Order Application", wx.OK | wx.ICON_INFORMATION)
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

    def OnInit(self):
        self.Bind(wx.EVT_ACTIVATE_APP, self.OnActivate)
        top = MainWindow(None)
        self.SetTopWindow(top)
        top.Show()
        return True

    def BringWindowsToFront(self):
        try:
            top = self.GetTopWindow()
            top.Raise()
        except:
            pass

    def OnActivate(self, event):
        if event.GetActive():
            self.BringWindowsToFront()
        event.Skip()

    def MacOpenFile(sel, filename):
        """Called for files dropped on dock icon or opened with context menu"""
        pass

    def MacReopenApp(self):
        """Called when the dock icon is clicked, maybe other times?"""
        self.BringWindowsToFront()

    def MacNewFile(self):
        pass

    def MacPrintFile(self, file_path):
        pass

if __name__ == "__main__":
    app = OrderApp(False)
    app.MainLoop()
