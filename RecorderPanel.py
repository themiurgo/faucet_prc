import wx
import sys
import PopMenuRecorder  # Classe che consente la visualizzazione di un menu' pop-up
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin,ColumnSorterMixin

# Dizionario pre-caricato per le prove
recordings = {
1 : ('Presa Diretta', 'Rai3', '15/02/2009','21:20','02:15','DivX','TV'),
2 : ('Viva Radio 2', 'Radio2', '16/02/2009','13:30','00:30','iPod','Radio')
}



#---------------------------------------------------------------------------

        
        
# Crea una lista Ordinabile e Auto-ridimensionabile grazie all'eredita' multipla        
class SortedListCtrl(wx.ListCtrl, ColumnSorterMixin,ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        ColumnSorterMixin.__init__(self, 7)
        ListCtrlAutoWidthMixin.__init__(self)
        self.itemDataMap = recordings

    def GetListCtrl(self):
        return self



#---------------------------------------------------------------------------



#Pannello (in alto) delle registrazioni puntate e da ultimare
class RecorderPanel(wx.Panel):
    def __init__(self, parent, id,panel,frame):
        wx.Panel.__init__(self, parent, -1)
        
        self.frame=frame
        self.panel=panel
        
        # Sizer, gestore del layout
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(panelSizer)
        
        header = wx.StaticText(self, -1, 'Registrazioni Programmate',style=wx.ALIGN_CENTER)
        header.Centre()
        panelSizer.Add(header,0,wx.EXPAND)
        
        
        # Crea la lista e aggiungi le colonne
        widthCol=90
        self.list =  SortedListCtrl(self)
        self.list.InsertColumn(0, 'Titolo', width=140)
        self.list.InsertColumn(1, 'Canale', width=widthCol)
        self.list.InsertColumn(2, 'Giorno', width=widthCol)
        self.list.InsertColumn(3, 'Inizio', width=widthCol)
        self.list.InsertColumn(4, 'Durata', width=widthCol)
        self.list.InsertColumn(5, 'Formato', width=widthCol)
        self.list.InsertColumn(6, 'Tipo', width=widthCol)
        
        
        # Risultato della funzione items() su vecchi dati di esempio
        # [(1, ('jessica','pomona','1981')]
        self.items = recordings.items()
        
        # Popola la lista con dati di esempio    
        for key, data in self.items:
            self.InsertValue(key,data)
        
        panelSizer.Add(self.list, 1, wx.EXPAND)
        
       
        self.list.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        
        self.SetBackgroundColour(wx.WHITE)
        
     #Crea il menu' pop-up alla pressione del tasto destro
    def OnRightDown(self,event):
        self.PopupMenu(PopMenuRecorder.PopMenuRecorder(self,self.panel,self.frame), event.GetPosition())
    
    # Inserisci un nuovo valore nella lista   
    def InsertValue(self,key,data):
        index = self.list.InsertStringItem(sys.maxint, data[0])
        self.list.SetStringItem(index, 1, data[1])
        self.list.SetStringItem(index, 2, data[2])
        self.list.SetStringItem(index, 3, data[3])
        self.list.SetStringItem(index, 4, data[4])
        self.list.SetStringItem(index, 5, data[5])
        self.list.SetStringItem(index, 6, data[6])
        #self.list.SetStringItem(index, 7, data[7])
        self.list.SetItemData(index, key)
    
    # Aggiorna il dizionario (necessario per coerenza sulla chiave)
    def UpdateItems(self,key,value):
        recordings[key]=value
            
    def GetMaxKey(self):
        return max(recordings.keys())

