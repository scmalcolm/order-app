'''
Bob Miller Book Room ordering application

Copyright Simon Malcolm 2012
'''
import wx
import layout
import model
from ObjectListView import ColumnDefn, ObjectListView

db_path = "/Users/bmbr/db/test.sqlite3"

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

class BookList(layout.BookListFrame):
    def __init__(self, parent):
        super(BookList, self).__init__(parent)

        columnList = [ColumnDefn("ISBN",      valueGetter="isbn13"),
                      ColumnDefn("Title",     valueGetter="title"),
                      ColumnDefn("Publisher", valueGetter="pub_name"),
                      ColumnDefn("Binding",   valueGetter="binding"),
                      ColumnDefn("Location",  valueGetter="location")]
        self.bookList.SetColumns(columnList)
        books = wx.GetApp().model.get_books()
        self.bookList.SetObjects(books)

    def OnOKButtonClick(self, event):
        self.Close()
        
class OrderApp(wx.App):

    def OnInit(self):
        self.model = model.OrderDB(db_path)
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

    def MacOpenFile(self, filename):
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
