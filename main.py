import wx
import model
from view.menu import MainWindow
from ObjectListView import ColumnDefn, ObjectListView

db_path = "/Users/bmbr/db/test.sqlite3"

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
