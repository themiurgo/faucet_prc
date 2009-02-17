import wx
import sys
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin
import PopMenuCompleted

STRING_WAITING='Disponibile'
STRING_AVAILABLE='In Attesa'
STRING_DOWNLOADED='Scaricato'

# Dizionario pre-caricato per le prove
recordings = {
0 : (STRING_DOWNLOADED, '1AnnoZero','Rai3', '08/02/2009','22:00','02:30','DivX','TV'),
1 : (STRING_WAITING, '2Hit List','RadioDJ', '13/02/2009','15:00','01:15','mp3','Radio'),
2 : (STRING_DOWNLOADED, '3Hit List','Virgin Radio', '13/02/2009','14:00','01:00','mp3','Radio'),
3 : (STRING_WAITING, '4AnnoZero','Rai3', '08/02/2009','22:00','02:30','DivX','TV'),
4 : (STRING_WAITING, '5AnnoZero','Rai3', '08/02/2009','22:00','02:30','DivX','TV'),
5 : (STRING_AVAILABLE, '6AnnoZero','Rai3', '08/02/2009','22:00','02:30','DivX','TV'),
6 : (STRING_DOWNLOADED, '7AnnoZero','Rai3', '08/02/2009','22:00','02:30','DivX','TV')
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
    def __init__(self, parent, id,panel,frame):
        wx.Panel.__init__(self, parent, -1)
        
        self.panel=panel
        self.frame=frame
        
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
        
        self.list.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        
        
     #Crea il menu' pop-up alla pressione del tasto destro
    def OnRightDown(self,event):
        self.PopupMenu(PopMenuCompleted.PopMenuCompleted(self,self.panel,self.frame), event.GetPosition())
        
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
        if data[0] == STRING_DOWNLOADED:
            self.SetCompleteColour(index)
    
    def SetCompleteColour(self,index):
        self.list.SetItemBackgroundColour(index,"light green")    
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

    def OnRemoveCompleted(self, event):
        num = self.list.GetItemCount()
        count=0
        for i in range(num):
            # Ottieni il testo di una colonna arbitraria
            #item = self.list.GetItem(i,4).GetText()
            itemStatus = self.list.GetItemText(i-count)
            # Obtain the key
            itemData = self.list.GetItemData(i-count)
            if itemStatus == STRING_DOWNLOADED:
                #print recordings[i]
              
                self.list.DeleteItem(i-count)
                count+=1; 
                del recordings[itemData]
       # print len(recordings)
                
                
            #print item
            #if self.list.IsChecked(i):
                #self.log.AppendText(self.list.GetItemText(i) + '\n')

