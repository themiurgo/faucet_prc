import wx
import wx.lib.masked as masked

typeReg=['Radio','TV']
stationTV=['Rai1','Rai2']
stationRadio=['Radio3','VirginRadio']
formatTV=['iPod','DivX']
formatRadio=['mp3']
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
        
            
        formatLabel = wx.StaticText(self, -1, "Formato di compressione:")
        formatLabel.SetHelpText("Help")
        
        formatCB = formatComboBox(self)
        formatCB.SetHelpText("Here's some help text for field #3")
        
        
        typeLabel = wx.StaticText(self, -1, "Tipo di registrazione")
        typeLabel.SetHelpText("Puo' essere 'Radio' o 'TV'")
        secondBox.Add(typeLabel, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        typeCB = typeComboBox(self,stationCB,formatCB)
        typeCB.SetHelpText("A seconda dell'opzione selezionata, si modificheranno i canali")
        secondBox.Add(typeCB, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
 
        
        #secondBox.Add(stationLabel, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        #secondBox.Add(stationCB, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        thirdBox = wx.BoxSizer(wx.HORIZONTAL)
        thirdBox.Add(stationLabel, 0, wx.ALIGN_CENTRE)
        thirdBox.Add(stationCB, 0, wx.ALIGN_CENTRE)
        

        fourthBox = wx.BoxSizer(wx.HORIZONTAL)
        fourthBox.Add(formatLabel, 0, wx.ALIGN_CENTRE)
        fourthBox.Add(formatCB, 0, wx.ALIGN_CENTRE)
        
        
        mainSizer.Add(secondBox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        mainSizer.Add(thirdBox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        mainSizer.Add(fourthBox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        
       
   # 3rd Level -------------------------------
        
        thirdBox = wx.BoxSizer(wx.HORIZONTAL)
        
        mainSizer.Add(thirdBox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        dateLabel = wx.StaticText(self, -1, "Giorno : ")
        dateLabel.SetHelpText("Help")
        thirdBox.Add(dateLabel, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        
        
        
        dpc = wx.DatePickerCtrl(self, size=(120,-1),
                                style = wx.DP_DROPDOWN
                                      | wx.DP_ALLOWNONE)
                                      #| wx.DP_ALLOWNONE )
        #self.Bind(wx.EVT_DATE_CHANGED, self.OnDateChanged, dpc)
        #sizer.Add(dpc, 0, wx.ALL, 50)

        if 'wxMSW' in wx.PlatformInfo:
            dpc = wx.GenericDatePickerCtrl(self, size=(120,-1),
                                           style = wx.DP_DROPDOWN
                                               | wx.DP_SHOWCENTURY
                                               | wx.DP_ALLOWNONE )
            self.Bind(wx.EVT_DATE_CHANGED, self.OnDateChanged, dpc)
            #sizer.Add(dpc, 0, wx.LEFT, 50)
            
        thirdBox.Add(dpc, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        
        spin2 = wx.SpinButton( self, -1, style=wx.SP_VERTICAL )
        time24 = masked.TimeCtrl(
                        self, -1, name="24 hour control", fmt24hr=True,
                        spinButton = spin2
                        )
                        
        hourLabel = wx.StaticText(self, -1, "Ora inizio : ")
        hourLabel.SetHelpText("Help")
        thirdBox.Add(hourLabel, 0, wx.ALIGN_CENTRE|wx.ALL, 5)                
        thirdBox.Add(time24, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        thirdBox.Add(spin2, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        sliderLabel = wx.StaticText(self, -1, "Durata : ")
        sliderLabel.SetHelpText("Help")
        thirdBox.Add(sliderLabel, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        slider = wx.Slider(
            self, 100, 25, 1, 100, (30, 60), (250, -1), 
            wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS 
            )

        slider.SetTickFreq(5, 1)
        
        thirdBox.Add(slider, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        

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

        mainSizer.Add(btnsizer, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        
    def GetValues(self):
        result = (self.text1.GetValue() ,self.text2.GetValue() ,self.text3.GetValue())
        return result
        
class typeComboBox(wx.ComboBox):
    def __init__(self,parent,stationCB,formatCB):
        wx.ComboBox.__init__(self,parent,value=NO_SELECTION,choices=typeReg,style=wx.CB_READONLY)
        
        self.stationCB=stationCB
        self.formatCB=formatCB
        #typeReg = ['Radio','TV']
        #self.SetValue(typeReg[1])

        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox)
    # When the user selects something, we go here.
    def EvtComboBox(self, evt):
        #cb = evt.GetEventObject()
        data = evt.GetString()
        self.stationCB.SetStations(data)
        self.formatCB.SetFormats(data)
        #print data
        
        
class stationComboBox(wx.ComboBox):
    def __init__(self,parent):
        wx.ComboBox.__init__(self,parent,value=NO_SELECTION,style=wx.CB_READONLY)
        
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
        
        
class formatComboBox(wx.ComboBox):
    def __init__(self,parent):
        wx.ComboBox.__init__(self,parent,value=NO_SELECTION,style=wx.CB_READONLY)
        
        #typeReg = ['Radio','TV']
        #self.SetValue(typeReg[1])

        #self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox)
    
    def SetFormats(self,stationType):
        self.Clear()
        self.SetValue(NO_SELECTION)
        if stationType == typeReg[0]:
            #self.Clear()
            self.AppendItems(formatRadio)
        elif stationType == typeReg[1]:
            self.AppendItems(formatTV)
        #cb = evt.GetEventObject()
        #data = evt.GetString()
        #print data
      

class SettingsDialog(wx.Dialog):
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self, parent, -1)
        
        sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, -1, "Impostazioni dell'account")
        label.SetHelpText("This is the help text for the label")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Username")
        label.SetHelpText("This is the help text for the label")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        text = wx.TextCtrl(self, -1, "", size=(80,-1))
        text.SetHelpText("Here's some help text for field #1")
        box.Add(text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Password")
        label.SetHelpText("This is the help text for the label")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        text = wx.TextCtrl(self, -1, "", size=(80,-1),style=wx.TE_PASSWORD)
        text.SetHelpText("Here's some help text for field #2")
        box.Add(text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()
        
        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        
        btn = wx.Button(self, wx.ID_OK)
        btn.SetHelpText("Salva i cambiamenti")
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btn.SetHelpText("Annulla i cambiamenti")
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)
