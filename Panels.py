import wx
import sys
import PopMenuRecorder
from wx.lib.mixins.listctrl import CheckListCtrlMixin,ListCtrlAutoWidthMixin,ColumnSorterMixin
import PopMenuCompleted
import vcast

STRING_WAITING='Disponibile'
STRING_AVAILABLE='In Attesa'
STRING_DOWNLOADED='Scaricato'

# Dizionario pre-caricato per le prove
#recordings_past = {
#0 : ('Presa Diretta', 'Rai3', '15/02/2009 21:20','02:15','DivX','TV'),
#1 : ('Viva Radio 2', 'Radio2', '16/02/2009 13:30','00:30','iPod','Radio')
#}

recordings_future = {
0 : (STRING_DOWNLOADED, '1AnnoZero','Rai3', '08/02/2009 22:00','02:30','DivX','TV'),
1 : (STRING_WAITING, '2Hit List','RadioDJ', '13/02/2009 15:00','01:15','mp3','Radio'),
2 : (STRING_DOWNLOADED, '3Hit List','Virgin Radio', '13/02/2009 14:00','01:00','mp3','Radio'),
3 : (STRING_WAITING, '4AnnoZero','Rai3', '08/02/2009 22:00','02:30','DivX','TV'),
4 : (STRING_WAITING, '5AnnoZero','Rai3', '08/02/2009 22:00','02:30','DivX','TV'),
5 : (STRING_AVAILABLE, '6AnnoZero','Rai3', '08/02/2009 22:00','02:30','DivX','TV'),
6 : (STRING_DOWNLOADED, '7AnnoZero','Rai3', '08/02/2009 22:00','02:30','DivX','TV')
}

# Sortable and auto-resizable list, multiple inheritance used
class SortedListCtrl(wx.ListCtrl, ColumnSorterMixin,
        ListCtrlAutoWidthMixin):

    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        ColumnSorterMixin.__init__(self, 6)
        ListCtrlAutoWidthMixin.__init__(self)
        self.itemDataMap = recordings_future

    def GetListCtrl(self):
        return self

# Panel of future recordings
class RecorderPanel(wx.Panel):
    def __init__(self, parent, id, panel, frame):
        wx.Panel.__init__(self, parent, -1)
        
        self.frame = frame
        self.panel = panel
        
        # Sizer, gestore del layout
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(panelSizer)
        
        header = wx.StaticText(self, -1, 'Registrazioni Programmate',
                style=wx.ALIGN_CENTER)
        header.Centre()
        panelSizer.Add(header,0,wx.EXPAND)
        
        # Crea la lista e aggiungi le colonne
        widthCol = 90
        self.list = SortedListCtrl(self)
        self.list.InsertColumn(0, 'Titolo', width=140)
        self.list.InsertColumn(1, 'Canale', width=widthCol)
        self.list.InsertColumn(2, 'Data', width=widthCol)
        self.list.InsertColumn(3, 'Durata', width=widthCol)
        self.list.InsertColumn(4, 'Formato', width=widthCol)
        self.list.InsertColumn(5, 'Tipo', width=widthCol)

        panelSizer.Add(self.list, 1, wx.EXPAND)
        self.list.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.SetBackgroundColour(wx.WHITE)
        self.Populate()

    def Populate(self):
        # Risultato della funzione items() su vecchi dati di esempio
        # [(1, ('jessica','pomona','1981')]
        reclist = vcast.i.get_recordings()
        # Vanno filtrati (futuri e passati) #TODO
        
        # Popola la lista con dati di esempio    
        print reclist
        for key, data in reclist.iteritems():
            self.InsertValue(key,data)
        
    # Inserisci un nuovo valore nella lista   
    def InsertValue(self,key,data):
        index = self.list.InsertStringItem(sys.maxint, data.title)
        self.list.SetStringItem(index, 1, data.channel)
        self.list.SetStringItem(index, 2, data.from_time)
        self.list.SetStringItem(index, 3, data.rec_time)
        self.list.SetStringItem(index, 4, data.format)
        self.list.SetStringItem(index, 5, data.channel_type)
        #self.list.SetStringItem(index, 6, data[6])
        #self.list.SetStringItem(index, 7, data[7])
        self.list.SetItemData(index, key)
    
    # Aggiorna il dizionario (necessario per coerenza sulla chiave)
    def UpdateItems(self, key, value):
        recordings_future[key]=value
            
    def GetMaxKey(self):
        return max(recordings_future.keys())

    # Contextual menu (on right click)
    def OnRightDown(self,event):
        self.PopupMenu(PopMenuRecorder.PopMenuRecorder(self, self.panel,
            self.frame), event.GetPosition())


# CheckBox provided and auto resizable list, used multiple inheritance
class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin,
        ListCtrlAutoWidthMixin):

    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, wx.ID_ANY,
                style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)
                
# Pannel of past recordings
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
        vbox.Add(header, 0, wx.EXPAND)
        
        # Crea l'oggetto CheckListCtrl e le relative colonne
        widthCol=90
        self.list = CheckListCtrl(self)
        self.list.InsertColumn(0, 'Stato', width=120)
        self.list.InsertColumn(1, 'Titolo', width=140)
        self.list.InsertColumn(2, 'Canale', width=widthCol)
        self.list.InsertColumn(3, 'Data', width=2*widthCol)
        #self.list.InsertColumn(4, 'Inizio', width=widthCol)
        self.list.InsertColumn(4, 'Durata', width=widthCol)
        self.list.InsertColumn(5, 'Formato', width=widthCol)
        self.list.InsertColumn(6, 'Tipo', width=widthCol)

        # Aggiunta della lista
        vbox.Add(self.list, 1, wx.EXPAND | wx.TOP)
        
        self.SetBackgroundColour(wx.LIGHT_GREY)
        self.list.SetBackgroundColour(wx.LIGHT_GREY)
        #vbox.Add((-1, 10))
        
        self.list.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

        # Aggiunta della lista
        #vbox.Add(self.list, 1, wx.EXPAND)
        
        self.Populate()

    def Populate(self):
        #for i in packages:
         #   index = self.list.InsertStringItem(sys.maxint, i[0])
          #  self.list.SetStringItem(index, 1, i[1])
           # self.list.SetStringItem(index, 2, i[2])
           
        # Routine per il popolamento delle colonne
        self.items = recordings_future.items()
        for key, data in self.items:
            self.InsertValue(key,data)

    # Contextual menu (right-click in the list)
    def OnRightDown(self,event):
        self.PopupMenu(PopMenuCompleted.PopMenuCompleted(self, self.panel,
            self.frame), event.GetPosition())
        
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
            
    def OnRemoveSelected(self, event):
        num = self.list.GetItemCount()
        count=0
        for i in range(num):
           if self.list.IsChecked(i-count):
                itemData = self.list.GetItemData(i-count)
                self.list.DeleteItem(i-count)
                count+=1; 
                del recordings_past[itemData]


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
                del recordings_past[itemData]
       # print len(recordings)
                
            #print item
            #if self.list.IsChecked(i):
                #self.log.AppendText(self.list.GetItemText(i) + '\n')
