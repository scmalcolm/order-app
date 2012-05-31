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
        self.selectedBook = None
        self.books = wx.GetApp().model.get_books()
        self.bookList.SetObjects(self.books)
        self.authorList.SetColumns([ColumnDefn("Name", width=50, valueGetter="author")])

    def OnOKButtonClick(self, event):
        self.Close()

    def OnDeleteBook(self, event):
        pass

    def OnSelectBook(self, event):
        isbn13 = self.bookList.GetSelectedObject()['isbn13']
        self.selectedBook = wx.GetApp().model.get_book(isbn13)
        self.RefreshEditPanel()
        self.bookEditPanel.Enable(True)

    def OnDeselectBook(self, event):
        self.selectedBook = None
        self.ClearEditPanel()
        self.bookEditPanel.Enable(False)

    def RefreshEditPanel(self):
        self.isbnText.SetValue(self.selectedBook['isbn13'])
        self.titleText.SetValue(self.selectedBook['title'])
        self.authorList.SetObjects([{'author': author} for author in self.selectedBook['authors']])
        self.publisherCombo.SetValue(self.selectedBook['pub_name'])
        self.bindingCombo.SetValue(self.selectedBook['binding'])
        self.locationCombo.SetValue(self.selectedBook['location'])

    def ClearEditPanel(self):
        self.isbnText.SetValue('')
        self.titleText.SetValue('')
        self.authorList.SetObjects([])
        self.publisherCombo.SetValue('')
        self.bindingCombo.SetValue('')
        self.locationCombo.SetValue('')

    def OnISBNEnter(self, event):
        new_isbn = self.isbnText.GetValue()
        old_isbn = self.selectedBook['isbn13']
        wx.GetApp().model.update_isbn(old_isbn, new_isbn)
        
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
