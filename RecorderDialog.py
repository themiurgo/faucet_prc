import wx

source=['Radio','TV']

# Questa classe rappresenta la finestra che crea una
# nuova registrazione. Ancora in fase di progettazione

class RecorderDialog(wx.Dialog):
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self, parent, -1,title="Creazione Nuova Registrazione")
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        header = wx.StaticText(self, -1, "Inserisci tutti i campi per creare\n la nuova registrazione",style=wx.ALIGN_CENTRE)
        header.SetHelpText("Per modificare i canali visualizzatti vai su preferenze")
        mainSizer.Add(header, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    # 1st Level -------------------------
        
        firstBox = wx.BoxSizer(wx.HORIZONTAL)

        title = wx.StaticText(self, -1, "Titolo")
        title.SetHelpText("Nome del programma che vuoi registrare")
        firstBox.Add(title, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        titleText = wx.TextCtrl(self, -1, "", size=(80,-1))
        titleText.SetHelpText("Nome del programma che vuoi registrare")
        firstBox.Add(titleText, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        #self.text1 = text       
        
        mainSizer.Add(firstBox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    
    
     # 2nd Level -------------------------
        
        secondBox = wx.BoxSizer(wx.HORIZONTAL)

        typeLabel = wx.StaticText(self, -1, "Tipo di registrazione")
        typeLabel.SetHelpText("Puo' essere 'Radio' o 'TV'")
        secondBox.Add(typeLabel, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        typeCB = typeComboBox(self)
        typeCB.SetHelpText("A seconda dell'opzione selezionata, si modificheranno i canali")
        secondBox.Add(typeCB, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        #self.text2=text
        
        mainSizer.Add(secondBox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        
        box = wx.BoxSizer(wx.HORIZONTAL)

        label4 = wx.StaticText(self, -1, "Field #3:")
        label4.SetHelpText("This is the help text for the label")
        box.Add(label4, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        text = wx.TextCtrl(self, -1, "", size=(80,-1))
        text.SetHelpText("Here's some help text for field #3")
        box.Add(text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.text3=text
        
        mainSizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        mainSizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()
        
        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        
        btn = wx.Button(self, wx.ID_OK)
        btn.SetHelpText("The OK button completes the dialog")
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btn.SetHelpText("The Cancel button cancels the dialog. (Cool, huh?)")
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        mainSizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        
        #self.text = text
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        
    def GetValues(self):
        result = (self.text1.GetValue() ,self.text2.GetValue() ,self.text3.GetValue())
        return result
        
class typeComboBox(wx.ComboBox):
    def __init__(self,parent):
        wx.ComboBox.__init__(self,parent,500,choices=source,style=wx.CB_READONLY)
        
        #source = ['Radio','TV']
        self.SetValue(source[1])

        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox)
    # When the user selects something, we go here.
    def EvtComboBox(self, evt):
        #cb = evt.GetEventObject()
        data = evt.GetString()
        #print data

        
