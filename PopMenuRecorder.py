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

        item1 = wx.MenuItem(self,wx.NewId(),
                "&Nuova Registrazione",
                "Elimina i download completati")
        iconPath ="./img/add.ico"
        icon = wx.Image(iconPath, wx.BITMAP_TYPE_ICO)
        item1.SetBitmap(wx.BitmapFromImage(icon)) 
        self.AppendItem(item1)
        
        

       # item1 = wx.MenuItem(self, , ")
        #self.AppendItem(item1)
        
        self.Bind(wx.EVT_MENU,  self.panel.OnAdd , item1)
        
        item2 = wx.MenuItem(self,wx.NewId(),
                "&Minimizza",
                "Minimizza la finestra")
        iconPath ="./img/minimize.ico"
        icon = wx.Image(iconPath, wx.BITMAP_TYPE_ICO)
        item2.SetBitmap(wx.BitmapFromImage(icon)) 
        self.AppendItem(item2)
        
        #item2 = wx.MenuItem(self, wx.NewId(),"")
        #self.AppendItem(item2)
        self.Bind(wx.EVT_MENU, self.OnItem2, item2)
        
        item3 = wx.MenuItem(self,wx.NewId(),
                "&Esci",
                "Abbandona Faucet PRC")
        iconPath ="./img/exit.ico"
        icon = wx.Image(iconPath, wx.BITMAP_TYPE_ICO)
        item3.SetBitmap(wx.BitmapFromImage(icon)) 
        self.AppendItem(item3)
        
        self.Bind(wx.EVT_MENU, self.frame.onCloseWindow, item3)

    #def OnItem1(self, event):
       # self.parent.OnAdd 

    def OnItem2(self, event):
        self.frame.Iconize()

    #def OnItem3(self, event):
     #   self.frame.closeWin
