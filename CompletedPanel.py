import wx
import sys
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin

# Dizionario pre-caricato per le prove
recordings = {
1 : ('Disponibile', 'AnnoZero','Rai3', '08/02/2009','22:00','02:30','DivX','TV'),
2 : ('In Attesa', 'Hit List','RadioDJ', '13/02/2009','15:00','01:15','mp3','Radio')
}



#---------------------------------------------------------------------------



# Costruisci una lista con CheckBox e Auto-Ridimensionata
# sfruttando l'ereditarieta' multipla
class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)
        
        
        
#---------------------------------------------------------------------------



#Pannello (in basso) delle registrazioni completate
class CompletedPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, -1)
        
        # Sizer, ovvero gestore del layout del pannello
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)
        
        # Crea e aggiungi l'intestazione
        header = wx.StaticText(self, -1, 'Registrazioni Completate',style=wx.ALIGN_CENTER)
        vbox.Add(header, 0, wx.EXPAND | wx.TOP)
        
        # Crea l'oggetto CheckListCtrl e le relative colonne
        widthCol=90
        self.list = CheckListCtrl(self)
        self.list.InsertColumn(0, 'Stato', width=120)
        self.list.InsertColumn(1, 'Titolo', width=140)
        self.list.InsertColumn(2, 'Canale', width=widthCol)
        self.list.InsertColumn(3, 'Giorno', width=widthCol)
        self.list.InsertColumn(4, 'Inizio', width=widthCol)
        self.list.InsertColumn(5, 'Durata', width=widthCol)
        self.list.InsertColumn(6, 'Formato', width=widthCol)
        self.list.InsertColumn(7, 'Tipo', width=widthCol)

        #for i in packages:
         #   index = self.list.InsertStringItem(sys.maxint, i[0])
          #  self.list.SetStringItem(index, 1, i[1])
           # self.list.SetStringItem(index, 2, i[2])
           
        # Routine per il popolamento delle colonne
        self.items = recordings.items()
        for key, data in self.items:
            self.InsertValue(key,data)

        # Aggiunta della lista
        vbox.Add(self.list, 1, wx.EXPAND | wx.TOP)
        
        self.SetBackgroundColour(wx.LIGHT_GREY)
        self.list.SetBackgroundColour(wx.LIGHT_GREY)
        #vbox.Add((-1, 10))
        
    def InsertValue(self,key,data):
        index = self.list.InsertStringItem(sys.maxint, data[0])
        self.list.SetStringItem(index, 1, data[1])
        self.list.SetStringItem(index, 2, data[2])
        self.list.SetStringItem(index, 3, data[3])
        self.list.SetStringItem(index, 4, data[4])
        self.list.SetStringItem(index, 5, data[5])
        self.list.SetStringItem(index, 6, data[6])
        self.list.SetStringItem(index, 7, data[7])
        self.list.SetItemData(index, key)
    
    # Studiare il funzionamento di queste funzioni per
    # capire come usare le caselle checkbox ... work in progress...    
    def OnSelectAll(self, event):
        num = self.list.GetItemCount()
        for i in range(num):
            self.list.CheckItem(i)

    def OnDeselectAll(self, event):
        num = self.list.GetItemCount()
        for i in range(num):
            self.list.CheckItem(i, False)

    def OnApply(self, event):
        num = self.list.GetItemCount()
        for i in range(num):
            if i == 0: self.log.Clear()
            if self.list.IsChecked(i):
                self.log.AppendText(self.list.GetItemText(i) + '\n')

