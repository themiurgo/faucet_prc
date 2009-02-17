import wx

typeReg=['Radio','TV']
stationTV=['Rai1','Rai2']
stationRadio=['Radio3','VirginRadio']
NO_SELECTION='---'

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
        
        stationLabel = wx.StaticText(self, -1, "Emittente:")
        stationLabel.SetHelpText("Radio o televisiva")
        

        stationCB = stationComboBox(self)
        stationCB.SetHelpText("Here's some help text for field #3")
        
        #self.text3=text
        
        typeLabel = wx.StaticText(self, -1, "Tipo di registrazione")
        typeLabel.SetHelpText("Puo' essere 'Radio' o 'TV'")
        secondBox.Add(typeLabel, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        typeCB = typeComboBox(self,stationCB)
        typeCB.SetHelpText("A seconda dell'opzione selezionata, si modificheranno i canali")
        secondBox.Add(typeCB, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        #self.text2=text
        
        secondBox.Add(stationLabel, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        secondBox.Add(stationCB, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        
        mainSizer.Add(secondBox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        
        box = wx.BoxSizer(wx.HORIZONTAL)

        
        
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
    def __init__(self,parent,stationCB):
        wx.ComboBox.__init__(self,parent,value=NO_SELECTION,choices=typeReg,style=wx.CB_READONLY)
        
        self.stationCB=stationCB
        #typeReg = ['Radio','TV']
        #self.SetValue(typeReg[1])

        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox)
    # When the user selects something, we go here.
    def EvtComboBox(self, evt):
        #cb = evt.GetEventObject()
        data = evt.GetString()
        self.stationCB.SetStations(data)
        #print data
        
        
class stationComboBox(wx.ComboBox):
    def __init__(self,parent):
        wx.ComboBox.__init__(self,parent,value=NO_SELECTION,choices=stationTV,style=wx.CB_READONLY)
        
        #typeReg = ['Radio','TV']
        #self.SetValue(typeReg[1])

        #self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox)
    
    def SetStations(self,stationType):
        self.Clear()
        self.SetValue(NO_SELECTION)
        if stationType == typeReg[0]:
            #self.Clear()
            self.AppendItems(stationRadio)
        elif stationType == typeReg[1]:
            self.AppendItems(stationTV)
        #cb = evt.GetEventObject()
        #data = evt.GetString()
        #print data

        
