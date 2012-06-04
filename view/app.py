'''
Bob Miller Book Room ordering application

Copyright Simon Malcolm 2012
'''
import wx
import layout
from .book import BookList
from ObjectListView import ColumnDefn, ObjectListView

class MainWindow(layout.MainFrame):

    def __init__(self, parent):
        layout.MainFrame.__init__(self, parent)
        wx.MenuBar.MacSetCommonMenuBar(self.menubar)
        
    def OnClose(self, event):
        if event.CanVeto():
            dlg = wx.MessageDialog(self, "Really Quit?", "Quit?",
                                   wx.YES_NO|wx.ICON_INFORMATION)
            confirm = dlg.ShowModal() == wx.ID_YES
            dlg.Destroy()
        if event.CanVeto() and not confirm:
            event.Veto()
        else:
            self.Destroy()
            event.Skip()

    def OnQuit(self, event):
        self.Close(force = True)

    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, "Bob Miller Book Room Orders\n"
                               "Application created by Simon Malcolm",
                               "Order Application", wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnHelp(self, event):
        dlg = wx.MessageDialog(self, "This would be help\n"
                                     "If there was any\n",
                               "Help", wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnPrefs(self, event):
        dlg = wx.MessageDialog(self, "Set Preferences here, eventually",
                               "Preferences", wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnViewBooks(self, event):
        dlg = BookList(self)
        dlg.Show()
        dlg.Raise()


