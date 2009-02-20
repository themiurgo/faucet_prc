import wx

#
# Crea un menu' pop-up, attualmente invocabile solo all'interno delle lista Superiore
#
# Il Costruttore prende in ingresso, oltre ai primi 2 tradizionali parametri, anche :
# 
# - panel : il pannello principale, cui appartiene la funzione 'OnAdd'
# - frame : la finestra principale del programma, per le 2 funzioni minimizza 
#           e chiudi
#
# Questi riferimenti sono necessari per invocare le funzioni
#
# NOTA: il costruttore e' invocato attualmente solo nella classe RecorderPanel.
# La ListCtrl e' ascoltatore dell'evento 'tasto destro del mouse', mentre
# il PopMenu stesso e' l'ascoltatore di eventi di tipo 'menu'. 
# In altre parole, la Lista fa aprire il menu' e il menu' decide che azione fare
# in base a cio' che si e' cliccato.
# 
class PopMenuRecorder(wx.Menu):
    def __init__(self,parent,panel,frame):
        wx.Menu.__init__(self)
        
        self.parent=parent
        self.panel=panel
        self.frame=frame

        self.Append(wx.ID_ADD,
                "A&ggiungi")
        
        
        
        self.Append(wx.ID_REFRESH,
                "&Aggiorna")
        
        self.AppendSeparator()
        
        item2 = wx.MenuItem(self,wx.NewId(),
                "&Minimizza",
                "Minimizza la finestra")
        iconPath ="./img/minimize.ico"
        icon = wx.Image(iconPath, wx.BITMAP_TYPE_ICO)
        item2.SetBitmap(wx.BitmapFromImage(icon)) 
        self.AppendItem(item2)
        
       
        self.Bind(wx.EVT_MENU, self.OnMinimize, item2)
        
        self.AppendSeparator()
        
        self.Append(wx.ID_EXIT,
                "&Esci")
        
        self.Bind(wx.EVT_MENU,  self.frame.OnAdd, id=wx.ID_ADD)
        self.Bind(wx.EVT_MENU, self.panel.OnRefresh, id=wx.ID_REFRESH)
        self.Bind(wx.EVT_MENU, self.frame.onCloseWindow, id=wx.ID_EXIT)

    
    def OnMinimize(self, event):
        self.frame.Iconize()


    #def OnItem3(self, event):
     #   self.frame.closeWin
