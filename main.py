#!/usr/bin/env python

import wx
import time
from Dialogs import *   # Finestra per l'inserimento di una nuova Registrazione
from Panels import *
# from taskbar import WxCastTaskBarIcon

# Codici utili per la gestione eventi
ID_ABOUT = 101
ID_EXIT = 110
ID_ACCOUNT = 120
ID_CHANNELS = 121

TBFLAGS = ( wx.TB_HORIZONTAL
            | wx.NO_BORDER
            | wx.TB_FLAT
            #| wx.TB_TEXT
            #| wx.TB_HORZ_LAYOUT
            )

# Questo oggetto consente la presenza di un help nelle varie finestre
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

#---------------------------------------------------------------------------

def OnTaskBarRight(event):
    self.ExitMainLoop()


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



#---------------------------------------------------------------------------
 
# Finestra Principale del Programma
class wxCastFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(800, 600))

#        self.DrawToolbar()
        
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

#        self.tbicon = WxCastTaskBarIcon(self)
#        self.tbicon.SetIconTimer()

#        wx.EVT_TASKBAR_RIGHT_UP(tbicon, OnTaskBarRight)
        
        self.Bind(wx.EVT_MENU, self.onMenuExit, id=ID_EXIT)
        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)

        #Centra e mostra il Frame
        self.Centre()
        self.Show(True)

    def DrawToolbar(self):
        tb = self.CreateToolBar(TBFLAGS)
        tsize = (24,24)
        new_bmp = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, tsize)
        open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
        copy_bmp = wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR, tsize)
        paste_bmp= wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_TOOLBAR, tsize)

        tb.SetToolBitmapSize(tsize)
        
        #tb.AddSimpleTool(10, new_bmp, "New", "Long help for 'New'")
        tb.AddLabelTool(10, "New", new_bmp, shortHelp="New", longHelp="Long help for 'New'")
        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=10)
        self.Bind(wx.EVT_TOOL_RCLICKED, self.OnToolRClick, id=10)

        #tb.AddSimpleTool(20, open_bmp, "Open", "Long help for 'Open'")
        tb.AddLabelTool(20, "Open", open_bmp, shortHelp="Open", longHelp="Long help for 'Open'")
        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=20)
        self.Bind(wx.EVT_TOOL_RCLICKED, self.OnToolRClick, id=20)

        tb.AddSeparator()
        tb.AddSimpleTool(30, copy_bmp, "Copy", "Long help for 'Copy'")
        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=30)
        self.Bind(wx.EVT_TOOL_RCLICKED, self.OnToolRClick, id=30)

        tb.AddSimpleTool(40, paste_bmp, "Paste", "Long help for 'Paste'")
        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=40)
        self.Bind(wx.EVT_TOOL_RCLICKED, self.OnToolRClick, id=40)

        tb.AddSeparator()

        # Final thing to do for a toolbar is call the Realize() method. This
        # causes it to render (more or less, that is).
        tb.Realize()

    def DoSearch(self,  text):
        # called by TestSearchCtrl
        self.log.WriteText("DoSearch: %s\n" % text)
        # return true to tell the search ctrl to remember the text
        return True
    

    def OnToolClick(self, event):
        self.log.WriteText("tool %s clicked\n" % event.GetId())
        #tb = self.GetToolBar()
        tb = event.GetEventObject()
        tb.EnableTool(10, not tb.GetToolEnabled(10))

    def OnToolRClick(self, event):
        self.log.WriteText("tool %s right-clicked\n" % event.GetId())

    def OnCombo(self, event):
        self.log.WriteText("combobox item selected: %s\n" % event.GetString())


    def onMenuExit(self,event):
        self.Close(True)

    # Chiudi la finestra + Finestra di conferma
    def onCloseWindow(self,e):
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
        val = dlg.Show(True)

        print dlg.GetReturnCode()

#        dlg.Show()
    
        #if val == wx.ID_OK:
            
        #else:
        #dlg.Destroy()

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
        self.recPanel = RecorderPanel(splitter, -1, self,self.parent)
        
        # Aggiungi (in basso) il pannello delle Registrazioni completate      
        self.comPanel = CompletedPanel(splitter, -1,self,self.parent)
        
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
        self.Bind(wx.EVT_BUTTON, self.comPanel.OnRemoveCompleted, clearButton)
        self.Bind(wx.EVT_BUTTON, self.comPanel.OnRemoveSelected, deleteButton)
        
        
    # Mostra la finestra per aggiungere una Registrazione
    def OnAdd(self, evt):
        recDialog = RecorderDialog(self, -1, "Crea un nuova Registrazione", size=(350, 200), style=wx.DEFAULT_DIALOG_STYLE)
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
