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
class PopMenuCompleted(wx.Menu):
    def __init__(self,parent,panel,frame):
        wx.Menu.__init__(self)
        
        self.parent=parent
        self.panel=panel
        self.frame=frame

        item1 = wx.MenuItem(self, wx.NewId(), "Rimuovi Completati")
        self.AppendItem(item1)
        #Per qualche motivo strano, se mettessi la chiamata 'OnAdd' nella
        #apposita funzione OnItem1, non funziona
        self.Bind(wx.EVT_MENU,  self.parent.OnRemoveCompleted , item1)
        
        item2 = wx.MenuItem(self, wx.NewId(),"Minimizza")
        self.AppendItem(item2)
        self.Bind(wx.EVT_MENU, self.OnItem2, item2)
        
        # Idem come sopra
        item3 = wx.MenuItem(self, wx.NewId(),"Chiudi")
        self.AppendItem(item3)
        self.Bind(wx.EVT_MENU, self.frame.onCloseWindow, item3)

    #def OnItem1(self, event):
       # self.parent.OnAdd 

    def OnItem2(self, event):
        self.frame.Iconize()

    #def OnItem3(self, event):
     #   self.frame.closeWin
