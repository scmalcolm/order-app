import wx

class AutoComboBox(wx.ComboBox) :
    def __init__(self, *args, **kwargs):
        super(AutoComboBox, self).__init__(*args, **kwargs)
        
        self.Bind(wx.EVT_CHAR, self.OnChar)
        self.Bind(wx.EVT_TEXT, self.OnText)

    def OnChar(self, event):
        print "OnChar"
        keycode = event.GetString()
        
        print "Keycode: {}".format(keycode)

        event.Skip()

    def OnText(self, event):
        print "OnText"

        event.Skip()