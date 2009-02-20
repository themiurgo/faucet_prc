import wx
import wx.lib.masked as masked
from datetime import datetime, timedelta
from vcast import Recording

STRING_TV="TV"
STRING_RADIO="Radio"

typeReg = [STRING_TV,STRING_RADIO]
formatTV = ['ipod','divx','appletv','psp','mp3']
formatRadio = ['mp3']
NO_SELECTION = ''

# Questa classe rappresenta la finestra che crea una
# nuova registrazione. Ancora in fase di progettazione

class RecorderDialog(wx.Dialog):
    def __init__(self, parent, ID, title, size=wx.DefaultSize,
            pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self, parent, -1,
                title="Creazione Nuova Registrazione")

        self.frame = parent

        (self.stationRadio, self.stationTV) = parent.interface.get_channels()

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        gridSizer= wx.FlexGridSizer(4,2,3,3)
    
    # TITLE -------------------------
        
        titleBox = wx.BoxSizer(wx.HORIZONTAL)

        self.titleLabel = wx.StaticText(self, -1, "Titolo : ")
        self.titleLabel.SetHelpText("Nome del programma che vuoi registrare")
        gridSizer.Add(self.titleLabel, 0, wx.ALIGN_LEFT|wx.ALL, 5)

        title = wx.TextCtrl(self, -1)
        title.SetHelpText("Nome del programma che vuoi registrare")
        gridSizer.Add(title, 0, wx.ALIGN_LEFT|wx.ALL|wx.GROW, 5)
        
        #mainSizer.Add(titleBox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    
    # TYPE STATION FORMAT -------------------------
        
        typeBox = wx.BoxSizer(wx.HORIZONTAL)
        
        stationLabel = wx.StaticText(self, -1, "Emittente :")
        stationLabel.SetHelpText("Radio o televisiva")
        
        typeLabel = wx.StaticText(self, -1, "Tipo di registrazione : ")
        typeLabel.SetHelpText("Puo' essere 'Radio' o 'TV'")
        gridSizer.Add(typeLabel, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        
        stationCB = StationComboBox(self)
        stationCB.SetHelpText("Nome dell'emittente")
            
        formatLabel = wx.StaticText(self, -1, "Formato di registrazione : ")
        formatLabel.SetHelpText("Seleziona il formato desiderato")
        
        formatCB = FormatComboBox(self)
        formatCB.SetHelpText("Seleziona fra le scelte disponibili")
        
        typeCB = TypeComboBox(self,stationCB,formatCB)
        typeCB.SetHelpText("A seconda dell'opzione selezionata, si modificheranno i canali")
        gridSizer.Add(typeCB, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        
        #secondBox.Add(stationLabel, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        #secondBox.Add(stationCB, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        stationBox = wx.BoxSizer(wx.HORIZONTAL)
        gridSizer.Add(stationLabel, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        gridSizer.Add(stationCB, 0, wx.ALIGN_LEFT|wx.ALL, 5)

        formatBox = wx.BoxSizer(wx.HORIZONTAL)
        gridSizer.Add(formatLabel, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        gridSizer.Add(formatCB, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        
    # DATE -------------------------------

        dateBox = wx.BoxSizer(wx.HORIZONTAL)
        
        dateLabel = wx.StaticText(self, -1, "Giorno : ")
        
        dateBox.Add(dateLabel, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        
        dpc = wx.DatePickerCtrl(self, size=(120,-1),
                style = wx.DP_DROPDOWN | wx.DP_ALLOWNONE)
        #self.Bind(wx.EVT_DATE_CHANGED, self.OnDateChanged, dpc)
        #sizer.Add(dpc, 0, wx.ALL, 50)
        dpc.SetHelpText("Giorno di inizio della registrazione")

        if 'wxMSW' in wx.PlatformInfo:
            dpc = wx.GenericDatePickerCtrl(self, size=(120,-1),
                    style = wx.DP_DROPDOWN | wx.DP_ALLOWNONE)
            self.Bind(wx.EVT_DATE_CHANGED, self.OnDateChanged, dpc)
            #sizer.Add(dpc, 0, wx.LEFT, 50)
            
        dateBox.Add(dpc, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        
        self.timeSpin = wx.SpinButton( self, -1, style=wx.SP_VERTICAL )
        self.time24 = masked.TimeCtrl(self, -1, name="24 hour control",
            fmt24hr=True, spinButton = self.timeSpin, display_seconds=False)
            
        self.time24.SetHelpText("Ora di inizio della registrazione")

        hourLabel = wx.StaticText(self, -1, "Ora inizio : ")
        hourLabel.SetHelpText("Help")
        dateBox.Add(hourLabel, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        dateBox.Add(self.time24, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        dateBox.Add(self.timeSpin, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
    # DURATION -------------------------------
        
        durationBox = wx.BoxSizer(wx.HORIZONTAL)
        durationGridSizer= wx.FlexGridSizer(1,2,1,1)
     
        self.slider = wx.Slider(
            self, -1, 30, 1, 180, (10, 10), (160, -1), 
             wx.SL_LABELS | wx.SL_TOP | wx.SL_HORIZONTAL | wx.SL_AUTOTICKS 
            )

        self.slider.SetTickFreq(1, 1)
        self.slider.SetHelpText("Durata (in minuti) della registrazione")
        
        self.Bind(masked.EVT_TIMEUPDATE, self.OnTimeUpdate)
        self.Bind(wx.EVT_SLIDER, self.OnTimeUpdate)
        #durationBox.Add(slider, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        durationGridSizer.Add(self.slider, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        
        #durationBox.AddSpacer(10,100000)
        durationBox.Add((30, 1))
       
        endLabel = wx.StaticText(self, -1, "Ora termine : ")
        endLabel.SetHelpText("Help")
        durationBox.Add(endLabel, 0, wx.ALIGN_LEFT|wx.TOP, 25)
        
        self.endTimeLabel = wx.StaticText(self, -1, "00:00:00")
        self.endTimeLabel.SetHelpText("Orario di termine della registrazione")
        self.endTimeLabel.SetHelpText("Help")
        durationBox.Add(self.endTimeLabel, 0, wx.ALIGN_LEFT|wx.TOP, 25)
         
        durationGridSizer.Add(durationBox, 0, wx.ALIGN_LEFT)
        
     # SLIDER -------------------------------
     
        sliderBox = wx.BoxSizer(wx.HORIZONTAL)
     
        sliderLabel = wx.StaticText(self, -1, "Durata (min)")
        sliderLabel.SetHelpText("Help")
        sliderBox.Add(sliderLabel, 0, wx.ALIGN_CENTER|wx.LEFT, 30)
       
    # Relative attrubutes
        self.title = title
        self.typeCB = typeCB
        self.stationCB = stationCB
        self.formatCB = formatCB
        self.dpc = dpc
        
     # BUTTONS  ----------------------------------
     
        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
          
         
        btnsizer = wx.StdDialogButtonSizer()
        
        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        
        ok = wx.Button(self, wx.ID_OK)
        ok.SetHelpText("Programma la registrazione")
        ok.SetDefault()
        btnsizer.AddButton(ok)

        btn = wx.Button(self, wx.ID_CANCEL)
        btn.SetHelpText("Annulla la registrazione")
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        
        mainSizer.Add(gridSizer, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        
        mainSizer.Add(dateBox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        
        mainSizer.Add(durationGridSizer, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        
        mainSizer.Add(sliderBox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        
        mainSizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)
        mainSizer.Add(btnsizer, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
       
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)

        # Initialize with default values
        t = datetime.now()
        delta = timedelta(minutes=10)
        t = t + delta
        text = datetime.strftime(t, "%H:%M:00")
        self.time24.SetValue(text)
        self.OnTimeUpdate(None)

        ok.Bind(wx.EVT_BUTTON, self.OnOk)
        
    def OnTimeUpdate(self, event):
        t = self.time24.GetValue()
        from_time = "2008-01-01 " + t
        d = datetime.strptime(from_time, "%Y-%m-%d %H:%M")
        delta = timedelta(minutes=self.slider.GetValue())
        d2 = d+delta
        to_time = datetime.strftime(d2, "%H:%M")
        self.endTimeLabel.SetLabel(to_time)

    def OnOk(self, event):
        if ( (self.title.GetValue() == "") | (self.stationCB.GetValue()=="") | (self.typeCB.GetValue()=="") | (self.formatCB.GetValue()=="") ):
            dlg = wx.MessageDialog(self, 'Devi riempire tutti i campi',
                               'Dati insufficienti',
                               wx.OK | wx.ICON_ERROR
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
            dlg.ShowModal()
            dlg.Destroy()
            
        else:
            t = self.time24.GetValue()
            from_time = "2009-02-20 " + t
            d = datetime.strptime(from_time, "%Y-%m-%d %H:%M")
            delta = timedelta(minutes=self.slider.GetValue())
            d2 = d + delta
            to_time = datetime.strftime(d2, "%H:%M")
            self.endTimeLabel.SetLabel(to_time)

            from_d = str(self.dpc.GetValue())
            
            from_date = datetime.strptime(from_d, "%a %d %b %Y 00:00:00 CET")
            t = self.time24.GetValue()
            delta = timedelta(hours=int(t[:2]), minutes=int(t[3:]))
            from_date = from_date + delta
            from_time = datetime.strftime(from_date, "%Y-%m-%d %H:%M:00")

            adate = datetime(2009,12,20)
            delta = timedelta(minutes=self.slider.GetValue())
            adate = adate + delta
            rec_time = datetime.strftime(adate, "%H:%M")
            
            if self.typeCB.GetValue() == STRING_TV:
                sendType = 'video'
            elif self.typeCB.GetValue() == STRING_RADIO:
                sendType = 'audio'

            r = Recording(-1, self.title.GetValue(), self.stationCB.GetValue(),
                    sendType, from_time,
                    rec_time, self.formatCB.GetValue())
            self.frame.interface.new_recording(r)
            self.frame.panel.OnRefresh(None)
            self.Destroy()

    def GetValues(self):
        result = (self.text1.GetValue() ,self.text2.GetValue() ,self.text3.GetValue())
        return result
        
class TypeComboBox(wx.ComboBox):
    def __init__(self,parent,stationCB,formatCB):
        wx.ComboBox.__init__(self, parent, value=NO_SELECTION,
                choices=typeReg, style=wx.CB_READONLY)
        
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
        
class StationComboBox(wx.ComboBox):
    def __init__(self,parent):
        wx.ComboBox.__init__(self,parent,value=NO_SELECTION,style=wx.CB_READONLY)

        self.parent = parent
        
        #typeReg = ['Radio','TV']
        #self.SetValue(typeReg[1])

        #self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox)
    
    def SetStations(self,stationType):
        self.Clear()
        self.SetValue(NO_SELECTION)
        if stationType == typeReg[1]:
            #self.Clear()
            self.AppendItems(self.parent.stationRadio)
        elif stationType == typeReg[0]:
            self.AppendItems(self.parent.stationTV)
        #cb = evt.GetEventObject()
        #data = evt.GetString()
        #print data

class FormatComboBox(wx.ComboBox):
    def __init__(self,parent):
        wx.ComboBox.__init__(self,parent, value=NO_SELECTION,
                style=wx.CB_READONLY)
    
    def SetFormats(self,stationType):
        self.Clear()
        self.SetValue(NO_SELECTION)
        if stationType == STRING_RADIO:
            #self.Clear()
            self.AppendItems(formatRadio)
        elif stationType == STRING_TV:
            self.AppendItems(formatTV)
        #cb = evt.GetEventObject()
        #data = evt.GetString()
        #print data

class SettingsDialog(wx.Dialog):
    def __init__(self, parent, ID, title, interface):
        wx.Dialog.__init__(self, parent, wx.ID_ANY,
                title="Impostazioni account")

        sizer = wx.BoxSizer(wx.VERTICAL)
        
        subsizer= wx.BoxSizer(wx.HORIZONTAL)
        
        link = wx.HyperlinkCtrl(self,-1,"vcast.it","http://www.vcast.it");
        label1 = wx.StaticText(self, -1,
            "Inserisci le tue credenziali Vcast.")
        #label.Wrap(250)
        sizer.Add(label1, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        label2 = wx.StaticText(self, -1,
            "Per registrarti, vai su :  ")
        
        subsizer.Add(label2, 0, wx.ALIGN_RIGHT)
        subsizer.Add(link, 0, wx.ALIGN_LEFT)
        
        sizer.Add(subsizer, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Username")
        label.SetHelpText("Inserisci il nome utente scelto durante la fase di registrazione al sito vcast")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.usr = wx.TextCtrl(self, -1, "", size=(80,-1))
        self.usr.SetHelpText("Inserisci il nome utente scelto durante la fase di registrazione al sito vcast")
        box.Add(self.usr, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Password")
        label.SetHelpText("Inserisci la password scelta durante la fase di registrazione al sito vcast")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.psw = wx.TextCtrl(self, -1, "", size=(80,-1),style=wx.TE_PASSWORD)
        self.psw.SetHelpText("Inserisci la password scelta durante la fase di registrazione al sito vcast")
        box.Add(self.psw, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, 
                wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()
        
        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        
        ok = wx.Button(self, wx.ID_OK)
        ok.SetHelpText("Salva i cambiamenti")
        ok.SetDefault()

        cancel = wx.Button(self, wx.ID_CANCEL)
        cancel.SetHelpText("Annulla i cambiamenti")

        btnsizer.AddButton(ok)
        btnsizer.AddButton(cancel)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)
        self.interface = interface
        try:
            account = self.interface.account
            self.usr.SetValue(account.username)
            self.psw.SetValue(account.password)
        except:
            pass

        ok.Bind(wx.EVT_BUTTON, self.updateAccount)

    def updateAccount(self, event):
        username = self.usr.GetValue()
        password = self.psw.GetValue()
        
        try:
            self.interface.setAccount(username,password)
            self.Destroy()
        except:
            dlg = wx.MessageDialog(self, 'Username o password errata.',
                    'Errore di login', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            

