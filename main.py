#!/usr/bin/env python

import wx
import time
import RecorderDialog   # Finestra per l'inserimento di una nuova Registrazione
import RecorderPanel    # Pannello delle registrazioni in corso o puntate
import CompletedPanel   # Pannello delle registrazioni completate

# Codici utili per la gestione eventi
ID_ABOUT = 101
ID_EXIT = 110
ID_ACCOUNT = 120
ID_CHANNELS = 121

# Questo oggetto consente la presenza di un help nelle varie finestre
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)



#---------------------------------------------------------------------------



# Fa visualizzare una schermata iniziale di caricamento
# Funzionalita' disabilitata di default (v. sotto)
def LoadingBar():
    timeLimit = 6
    loadingDlg = wx.ProgressDialog("Benvenuto in wxCast!", "Caricamento in corso...", maximum = max, parent=None, style = wx.PD_AUTO_HIDE | wx.PD_REMAINING_TIME )
    #Ulteriori Opzioni per la finestra
    #|wx.PD_CAN_ABORT | wx.PD_APP_MODAL  | wx.PD_ELAPSED_TIME | wx.PD_ESTIMATED_TIME
    
    keepGoing = True
    time = 0
    while keepGoing and time < timeLimit:
        time += 1
        wx.MilliSleep(250)

        if count >= timeLimit / 1.3:
            (keepGoing, skip) = loadingDlg.Update(time,"Quasi finito!")      
        else:
            (keepGoing, skip) = loadingDlg.Update(time)
    loadingDlg.Destroy()     



#---------------------------------------------------------------------------




class MainMenuBar(wx.MenuBar):
    def __init__(self, frame):
        wx.MenuBar.__init__(self)

        # Menu (I livello)
        filemenu = wx.Menu()
        impostazioni = wx.Menu()

        # Sottomenu FILE
        filemenu.Append(ID_ABOUT,
                "&Informazioni\tCTRL+I",
                "Informazioni sull'applicazione")
        filemenu.AppendSeparator()
        filemenu.Append(ID_EXIT,
                "&Esci\tCTRL+Q",
                "Esci dall'applicazione")
        self.Append(filemenu, "&File")

        # Sottomenu IMPOSTAZIONI
        self.Append(impostazioni, "&Impostazioni")
        impostazioni.Append(ID_ACCOUNT,
                "&Account\tCTRL+A",
                "Imposta le credenziali dell'account Vcast")
        impostazioni.Append(ID_CHANNELS,
                "&Canali\tCTRL+H",
                "Imposta le preferenze sui canali")

        frame.Bind(wx.EVT_MENU, frame.closeWin, id=ID_EXIT)
        frame.Bind(wx.EVT_MENU, frame.Settings, id=ID_ACCOUNT)



#---------------------------------------------------------------------------



class MainStatusBar(wx.StatusBar):
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, -1)

        # This status bar has two fields
        self.SetFieldsCount(3)
        # Sets the three fields to be relative widths to each other.
        self.SetStatusWidths([-2, -2, -1])
        self.sizeChanged = False
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_IDLE, self.OnIdle)

        # Field 0 ... just text
        self.SetStatusText("Nessuna registrazione disponibile", 1)

        # set the initial position of the checkbox
        self.Reposition()

        # We're going to use a timer to drive a 'clock' in the last
        # field.
        self.timer = wx.PyTimer(self.Notify)
        self.timer.Start(1000)
        self.Notify()

    # Handles events from the timer we started in __init__().
    # We're using it to drive a 'clock' in field 2 (the third field).
    def Notify(self):
        t = time.localtime(time.time())
        st = time.strftime("%d-%b-%Y   %I:%M:%S", t)
        self.SetStatusText(st, 2)

    def OnSize(self, evt):
        self.Reposition()  # for normal size events

        # Set a flag so the idle time handler will also do the repositioning.
        # It is done this way to get around a buglet where GetFieldRect is not
        # accurate during the EVT_SIZE resulting from a frame maximize.
        self.sizeChanged = True

    def OnIdle(self, evt):
        if self.sizeChanged:
            self.Reposition()

    # reposition the checkbox
    def Reposition(self):
        rect = self.GetFieldRect(1)
        self.sizeChanged = False




#---------------------------------------------------------------------------



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



#---------------------------------------------------------------------------


 
# Finestra Principale del Programma
class wxCastFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(800, 600))
        
        #Aggiungi il pannello che contiene bottoni e schede
        self.panel = MainPanel(self,id)
        
        #Creazione StatusBar 
        statusbar = MainStatusBar(self)
        self.SetStatusBar(statusbar)
          
        menubar = MainMenuBar(self)
        self.SetMenuBar(menubar)
    
        
        #Aggiungi l'icona
        iconPath ="./img/fau_icon.ico"
        icon = wx.Icon(iconPath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        
        #Centra e mostra il Frame
        self.Centre()
        self.Show(True)

    # Chiudi la finestra + Finestra di conferma
    def closeWin(self,e):
        confirmDialog = wx.MessageDialog(None, 'Sei sicuro di voler uscire?', 'Abbandona wxCast', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        
        # Finestra di conferma
        choice = confirmDialog.ShowModal()
        if choice == wx.ID_YES:#5103:
            self.Destroy()
        #else:
        confirmDialog.Destroy()
    
    def Settings(self, event):

            
        dlg = SettingsDialog(self, -1, "Account", size=(500, 200),
                         #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
                         style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX          
                         )
        dlg.CenterOnScreen()

        # this does not return until the dialog is closed.
        val = dlg.ShowModal()
    
        #if val == wx.ID_OK:
            
        #else:
            

        dlg.Destroy()
        


#---------------------------------------------------------------------------    




# Pannello principale del Frame        
class MainPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, -1)
        self.parent=parent
        
        # Crea il gestore principale del layout nel pannello
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)
        
        # Crea il bottone per aggiungere un nuovo programma da registrare
        addButton = wx.Button(self, wx.ID_ADD)
        mainSizer.Add(addButton)
        
        #Crea lo splitter, che contiene i due pannelli ridimensionabili
        splitter = wx.SplitterWindow(self,style=wx.SP_LIVE_UPDATE)
        splitter.SetMinimumPaneSize(20)  #Dimensione minima ammissibile per i tab
        self.splitter = splitter
        mainSizer.Add(splitter, 1, wx.EXPAND) #Aggiunge lo splitter
        
        # Aggiungi (in alto) il pannello delle Registrazioni da completare      
        self.recPanel = RecorderPanel.RecorderPanel(splitter, -1, self,self.parent)
        
        # Aggiungi (in basso) il pannello delle Registrazioni completate      
        self.comPanel = CompletedPanel.CompletedPanel(splitter, -1)
        
        splitter.SplitHorizontally(self.recPanel, self.comPanel)
        
        #Aggiungi i due bottoni per l'eliminazione ed il download dei file
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        deleteButton = wx.Button(self, wx.ID_DELETE)
        clearButton = wx.Button(self, wx.ID_CLEAR)
        saveButton = wx.Button(self, wx.ID_SAVE)
        bottomSizer.Add(deleteButton)
        bottomSizer.Add(clearButton)
        bottomSizer.Add(saveButton)
        mainSizer.Add(bottomSizer,0)
        
        #Associa un'azione ai bottoni
        self.Bind(wx.EVT_BUTTON, self.OnAdd, addButton)
        
        
    # Mostra la finestra per aggiungere una Registrazione
    def OnAdd(self, evt):
        recDialog = RecorderDialog.RecorderDialog(self, -1, "Crea un nuova Registrazione", size=(350, 200), style=wx.DEFAULT_DIALOG_STYLE)
        recDialog.CenterOnScreen()

        # Per capire se l'utente ha premuto Ok o Abort
        choice = recDialog.ShowModal()
    
        if choice == wx.ID_OK:
            data = recDialog.GetValues()        # Ottieni il valore di tutti i campi
            maxKey = self.recPanel.GetMaxKey()  # Ottieni il max indice
            maxKey=maxKey+1
            # Inserisci la nuova registrazione nella lista
            self.recPanel.UpdateItems(maxKey,data) 
            self.recPanel.InsertValue(maxKey,data)
        #else:
        recDialog.Destroy()



#---------------------------------------------------------------------------



if __name__ == '__main__':
    app = wx.App()
    #Decommenta per far visualizzare una barra di caricamento iniziale
    #LoadingBar()
    #frame = MainFrame(None,
     #           wx.ID_ANY,
      #          title="Faucet PRC (Private Remote Contol)",
       #         size=(800,600),
        #        style=wx.DEFAULT_FRAME_STYLE)
    wxCastFrame(None, -1, 'wxCast')
    app.MainLoop()

