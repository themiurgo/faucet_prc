#!/usr/bin/env python

import wx
import time
from Dialogs import *
from Panels import *
import vcast
import webbrowser

ID_INFO = 101
ID_ABOUT = 105
ID_EXIT = 110
ID_ACCOUNT = 120
ID_CHANNELS = 121

# Provides contextual help in the program
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

class MainMenuBar(wx.MenuBar):
    def __init__(self, frame):
        wx.MenuBar.__init__(self)

        # Menu (I livello)
        filemenu = wx.Menu()
        impostazioni = wx.Menu()
        about = wx.Menu()

        # Sottomenu FILE
        item = wx.MenuItem(filemenu,ID_INFO,
                "&Informazioni\tCTRL+I",
                "Informazioni sull'applicazione")
        iconPath ="./img/info.ico"
        icon = wx.Image(iconPath, wx.BITMAP_TYPE_ICO)
        item.SetBitmap(wx.BitmapFromImage(icon)) 
        filemenu.AppendItem(item)
        filemenu.AppendSeparator()
        
        item = wx.MenuItem(filemenu,ID_EXIT,
                "&Esci\tCTRL+Q",
                "Esci dall'applicazione")
        iconPath ="./img/exit.ico"
        icon = wx.Image(iconPath, wx.BITMAP_TYPE_ICO)
        item.SetBitmap(wx.BitmapFromImage(icon)) 
        filemenu.AppendItem(item)
        #filemenu.Append()
        self.Append(filemenu, "&File")

        # Sottomenu IMPOSTAZIONI
        self.Append(impostazioni, "&Impostazioni")
        
        item = wx.MenuItem(impostazioni,ID_ACCOUNT,
                "&Account\tCTRL+A",
                "Imposta le credenziali dell'account Vcast")
        iconPath ="./img/userinfo.ico"
        icon = wx.Image(iconPath, wx.BITMAP_TYPE_ICO)
        item.SetBitmap(wx.BitmapFromImage(icon)) 
        impostazioni.AppendItem(item)
       
        
        impostazioni.Append(ID_CHANNELS,
                "&Canali\tCTRL+H",
                "Imposta le preferenze sui canali")
        
        # Sottomenu ABOUT
        self.Append(about, "&?")
        about.Append(ID_ABOUT,
                "A&bout\tCTRL+B",
                "Informazioni su Faucet PRC")

        frame.Bind(wx.EVT_MENU, frame.Settings, id=ID_ACCOUNT)

class MainStatusBar(wx.StatusBar):
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, -1)

        # Statusbar with 3 fields
        self.SetFieldsCount(3)

        # Relative widths of fields
        self.SetStatusWidths([-2, -2, -1])
        self.sizeChanged = False

        # Field 0: downloadable recordings status
        self.SetStatusText("Nessuna registrazione disponibile", 1)

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

# Finestra Principale del Programma
class faucetPRCFrame(wx.Frame):
    def __init__(self, parent, id, title, interface):
        wx.Frame.__init__(self, parent, id, title, size=(800, 600))

        # self.DrawToolbar()
        self.interface = interface
        
        # Main Panel
        MainPanel(self,id)
        
        #sizer = wx.BoxSizer(wx.VERTICAL)
        #sizer.Add(panel,1,wx.EXPAND)
        #self.SetSizerAndFit(sizer)

        # StatusBar and MenuBar 
        self.SetStatusBar(MainStatusBar(self))
        self.SetMenuBar(MainMenuBar(self))
        
        # Icon
        iconPath = "./img/fau_icon.ico"
        icon = wx.Icon(iconPath, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        self.Bind(wx.EVT_MENU, self.onMenuExit, id=ID_EXIT)
        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)

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
        confirmDialog = wx.MessageDialog(None, 'Sei sicuro di voler uscire?', 'Abbandona Faucet PRC', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        
        # Finestra di conferma
        choice = confirmDialog.ShowModal()
        if choice == wx.ID_YES:#5103:
            self.Destroy()
        #else:
        confirmDialog.Destroy()
    
    def Settings(self, event):
        dlg = SettingsDialog(self, -1, "Account", self.interface)
        dlg.CenterOnScreen()

        val = dlg.Show(True)

# Main Panel
class MainPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, -1)
        self.parent = parent
        
        # Crea il gestore principale del layout nel pannello
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)
        
        # Upper Buttons
        upSizer = wx.BoxSizer(wx.HORIZONTAL)
        addButton = wx.Button(self, wx.ID_ADD)
        refreshButton = wx.Button(self, wx.ID_REFRESH)
        deleteButton = wx.Button(self, wx.ID_REMOVE)
        upSizer.Add(addButton)
        upSizer.Add(refreshButton)
        upSizer.Add(deleteButton)
        mainSizer.Add(upSizer)
        refreshButton.Bind(wx.EVT_BUTTON, self.OnRefresh)
        
        #Crea lo splitter, che contiene i due pannelli ridimensionabili
        splitter = wx.SplitterWindow(self,style=wx.SP_LIVE_UPDATE)
        splitter.SetMinimumPaneSize(20)  #Dimensione minima ammissibile per i tab
        self.splitter = splitter
        mainSizer.Add(splitter, 1, wx.EXPAND) #Aggiunge lo splitter
        
        # Recording panels
        self.comPanel = CompletedPanel(splitter, -1, self, self.parent)
        self.recPanel = RecorderPanel(splitter, -1, self,self.parent)

        vcast.i.get_recordings()
        self.recPanel.Populate(vcast.i.getFutureRecordings())
        self.comPanel.Populate(vcast.i.getPastRecordings())
        
        splitter.SplitHorizontally(self.recPanel, self.comPanel)
        
        #Aggiungi i due bottoni per l'eliminazione ed il download dei file
        #deleteButton = wx.Button(self, wx.ID_DELETE)
        #clearButton = wx.Button(self, wx.ID_CLEAR)
        saveButton = wx.Button(self, wx.ID_SAVEAS)
        #upperSizer.Add(deleteButton,0,wx.EXPAND)
        #upperSizer.Add(clearButton,0,wx.EXPAND)
        upSizer.Add(saveButton,0,wx.EXPAND)
        
        #Associa un'azione ai bottoni
        addButton.Bind(wx.EVT_BUTTON, self.OnAdd)
        #clearButton.Bind(wx.EVT_BUTTON, self.comPanel.OnRemoveCompleted)
        #deleteButton.Bind(wx.EVT_BUTTON, self.comPanel.OnRemoveSelected)
        saveButton.Enable(False)
        saveButton.Bind(wx.EVT_BUTTON, self.OnSaveAs)

        self.saveButton = saveButton
        
    # Mostra la finestra per aggiungere una Registrazione
    def OnAdd(self, evt):
        recDialog = RecorderDialog(self, -1, "Crea un nuova Registrazione", size=(350, 200), style=wx.DEFAULT_DIALOG_STYLE)
        recDialog.CenterOnScreen()

        # Per capire se l'utente ha premuto Ok o Abort
        choice = recDialog.ShowModal()
    
        if choice == wx.ID_OK:
            data = recDialog.GetValues()        # Ottieni il valore di tutti i campi
            maxKey = self.recPanel.GetMaxKey()  # Ottieni il max indice
            maxKey += 1
            # Inserisci la nuova registrazione nella lista
            self.recPanel.UpdateItems(maxKey,data) 
            self.recPanel.InsertValue(maxKey,data)
        #else:
        recDialog.Destroy()

    def OnRefresh(self, event):
        try:
            recs = vcast.i.get_recordings()
            self.recPanel.Clear()
            self.comPanel.Clear()
            self.recPanel.Populate(recs)
            self.recPanel.TransferOld()
        except:
            print "Error"

    def OnSaveAs(self,event):
        list = self.comPanel.list
        position = list.GetFirstSelected() # Position in the ListCtrl
        id = list.GetItemData(position) # Unique ID
        url = vcast.i.recordings[id].url
        print id, position, vcast.i.recordings[id].url
        webbrowser.open(url)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    app = wx.App()
    #Decommenta per far visualizzare una barra di caricamento iniziale
    #LoadingBar()

    # Interface of Vcast API
    vcast.i = vcast.Interface()
    try:
        vcast.i.setAccount('4nT0','eyeswideshut')
    except:
        raise "Wrong credentials"
        # Visualizza il dialogo delle impostazioni
        sys.exit(1)
    
    # First, try to load recordings and account informations
    # If no preferences, launch Wizard
    try:
        vcast.i.loadFile()
    except:
        print "Wizard"
        # Set username and password

    faucetPRCFrame(None, wx.ID_ANY, 'Faucet PRC',vcast.i)
    app.MainLoop()
