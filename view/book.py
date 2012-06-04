import wx
from . import layout
from ObjectListView import ColumnDefn, ObjectListView

class BookList(layout.BookListFrame):
    def __init__(self, *args, **kwargs):
        super(BookList, self).__init__(*args, **kwargs)

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

class BookCreator(layout.NewBookFrame):
    """docstring for BookCreator"""
    def __init__(self, *args, **kwargs):
        super(BookCreator, self).__init__(*args, **kwargs)

        self._initAuthorList()
        self._initComboControls()

    def _initAuthorList(self):
        columnList = [ColumnDefn("Name", width = 50, valueGetter = "author")]
        self.authorList.SetColumns(columnList)

    def _initComboControls(self):
        publishers = wx.GetApp().model.publishers()
        bindings = wx.GetApp().model.bindings()
        locations = wx.GetApp().model.locations()
        self.publisherCombo.SetItems(publishers)
        self.bindingCombo.SetItems(bindings)
        self.locationCombo.SetItems(locations)

