import wx
import sys
import PopMenuRecorder
from wx.lib.mixins.listctrl import CheckListCtrlMixin,ListCtrlAutoWidthMixin,ColumnSorterMixin
import PopMenuCompleted
import vcast
from datetime import datetime, timedelta

STRING_WAITING='In lavorazione'
STRING_AVAILABLE='Disponibile'
STRING_DOWNLOADED='Scaricato'
PastRecordings={}
FutureRecordings={}

# Sortable and auto-resizable list, multiple inheritance used
class SortedListCtrl(wx.ListCtrl, ColumnSorterMixin,
        ListCtrlAutoWidthMixin):

    def __init__(self, parent,col,panelType):
        wx.ListCtrl.__init__(self, parent, -1,
                style=wx.LC_REPORT | wx.SUNKEN_BORDER | wx.LC_SINGLE_SEL)
        self.SetSingleStyle(wx.LC_HRULES, True)
        ColumnSorterMixin.__init__(self, col)
        ListCtrlAutoWidthMixin.__init__(self)
        if panelType==0:
            self.itemDataMap = PastRecordings
        elif panelType==1:
            self.itemDataMap = FutureRecordings
              
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
        
        self.header = wx.StaticText(self, -1, 'Registrazioni Programmate',
                style=wx.ALIGN_CENTER)

        panelSizer.Add(self.header,0,wx.EXPAND|wx.ALIGN_CENTER)

        self.header.Fit()
        self.header.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        panelSizer.Add(self.header,0,wx.EXPAND)
        panelSizer.Add((-1, 4))
        
        # Crea la lista e aggiungi le colonne
        widthCol = 90
        self.list = SortedListCtrl(self,6,0)
        self.list.InsertColumn(0, 'Titolo', width=140)
        self.list.InsertColumn(1, 'Canale', width=widthCol)
        self.list.InsertColumn(2, 'Data', width=2*widthCol)
        self.list.InsertColumn(3, 'Durata', width=widthCol)
        self.list.InsertColumn(4, 'Formato', width=widthCol)
        self.list.InsertColumn(5, 'Tipo', width=widthCol)
         
       
        panelSizer.Add(self.list, 1, wx.EXPAND)
        self.list.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

        self.list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.list.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselect)

        self.timer = wx.PyTimer(self.TransferOld)
        self.timer.Start(30000)

    def Clear(self):
        self.list.DeleteAllItems()

    def Populate(self, values):
        for key, data in values.iteritems():
            self.InsertValue(key,data)

    def TransferOld(self):
        """Removes from the list old recordings"""
        num = self.list.GetItemCount()
        colsN = self.list.GetColumnCount()
        r = range(num)
        r.reverse()
        for i in r:
            from_time_s = self.list.GetItem(i,2).GetText()
            from_time = datetime.strptime(from_time_s, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            if from_time < now:
                k = self.panel.comPanel.list.InsertItem(
                        self.list.GetItem(i,0))
                for j in range(1,colsN):
                    self.panel.comPanel.list.SetStringItem(k, j,
                            self.list.GetItem(i,j).GetText())
                self.list.DeleteItem(i)
                #print i
                key = self.list.GetItemData(i)
                self.panel.OnRefresh(None)
                
    #def RemoveValueFromDictionary(self,key):
        #del PastRecordings[key]
        
        
    # Inserisci un nuovo valore nella lista   
    def InsertValue(self,key,data):
        PastRecordings[key]=(data.title,data.channel,data.from_time,data.rec_time,data.format,data.channel_type)
        index = self.list.InsertStringItem(sys.maxint, data.title)
        self.list.SetStringItem(index, 1, data.channel)
        self.list.SetStringItem(index, 2, data.from_time)
        self.list.SetStringItem(index, 3, data.rec_time)
        self.list.SetStringItem(index, 4, data.format)
        self.list.SetStringItem(index, 5, data.channel_type)
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

    def OnItemSelected(self, event):
        self.panel.comPanel.list.Select(
                self.panel.comPanel.list.GetFirstSelected(),on=0)
        #self.panel.saveButton.Enable(False)
        self.frame.tb.EnableTool(wx.ID_SAVEAS, False)
        self.frame.tb.EnableTool(wx.ID_REMOVE, True)

    def OnItemDeselect(self, event):
        if (self.panel.comPanel.list.GetFirstSelected() < 0
                and self.panel.recPanel.list.GetFirstSelected() < 0):
            self.frame.tb.EnableTool(wx.ID_REMOVE, False)

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
        self.avaibleN = 0 # Number of avaible downloads
        
        # Sizer, ovvero gestore del layout del pannello
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)
        
        # Crea e aggiungi l'intestazione
        header = wx.StaticText(self, -1, 'Registrazioni Completate',
                style=wx.ALIGN_CENTER)
        header.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        vbox.Add((-1, 10))
        vbox.Add(header, 0, wx.EXPAND)
        vbox.Add((-1, 4))
        
        # Crea l'oggetto CheckListCtrl e le relative colonne
        widthCol=90
        self.list = SortedListCtrl(self,7,1)
        self.list.InsertColumn(0, 'Titolo', width=140)
        self.list.InsertColumn(1, 'Canale', width=widthCol)
        self.list.InsertColumn(2, 'Data', width=2*widthCol)
        self.list.InsertColumn(3, 'Durata', width=widthCol)
        self.list.InsertColumn(4, 'Formato', width=widthCol)
        self.list.InsertColumn(5, 'Tipo', width=widthCol)
        self.list.InsertColumn(6, 'Stato', width=120)

        # Aggiunta della lista
        vbox.Add(self.list, 1, wx.EXPAND | wx.TOP)
        
        self.list.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.list.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselect)

        # Aggiunta della lista
        #vbox.Add(self.list, 1, wx.EXPAND)
        
#        self.Populate()

    def Populate(self, values):
        #for i in packages:
         #   index = self.list.InsertStringItem(sys.maxint, i[0])
          #  self.list.SetStringItem(index, 1, i[1])
           # self.list.SetStringItem(index, 2, i[2])
           
        # Routine per il popolamento delle colonne
        self.items = values.iteritems()
        self.avaibleN = 0
        for key, data in self.items:
            self.InsertValue(key,data)
        if self.avaibleN != 0:
            self.frame.sb.SetStatusText(str(self.avaibleN) +
                    " registrazioni pronte ad essere scaricate", 1)
        else:
            self.frame.sb.SetStatusText(
                    "Nessuna registrazione disponibile", 1)

    def Clear(self):
        self.list.DeleteAllItems()

    # Contextual menu (right-click in the list)
    def OnRightDown(self,event):
        self.PopupMenu(PopMenuCompleted.PopMenuCompleted(self, self.panel,
            self.frame), event.GetPosition())
        
    def InsertValue(self,key,data):
        index = self.list.InsertStringItem(sys.maxint, data.title)
        self.list.SetStringItem(index, 1, data.channel)
        self.list.SetStringItem(index, 2, data.from_time)
        self.list.SetStringItem(index, 3, data.rec_time)
        self.list.SetStringItem(index, 4, data.format)
        self.list.SetStringItem(index, 5, data.channel_type)
        if data.url != None:
            self.list.SetStringItem(index, 6, STRING_AVAILABLE)
            self.avaibleN += 1
            final = STRING_AVAILABLE
        else:
            final = STRING_WAITING
            self.list.SetStringItem(index, 6, STRING_WAITING)
        self.list.SetItemData(index, key)
        if False:
            self.SetCompleteColour(index)
        FutureRecordings[key]=(data.title,data.channel,data.from_time,data.rec_time,data.format,data.channel_type,final)
    
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
                #del FutureRecordings[itemData]

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

    def OnItemSelected(self, event):
        self.frame.tb.EnableTool(wx.ID_REMOVE, True)
        self.panel.recPanel.list.Select(
                self.panel.recPanel.list.GetFirstSelected(),on=0)
        position = self.list.GetFirstSelected() # Position in the ListCtrl
        id = self.list.GetItemData(position) # Unique ID
        url = vcast.i.recordings[id].url
        if url != None:
            #self.panel.saveButton.Enable(True)
            self.frame.tb.EnableTool(wx.ID_SAVEAS, True)
        else:
            #self.panel.saveButton.Enable(False)
            self.frame.tb.EnableTool(wx.ID_SAVEAS, False)

    def OnItemDeselect(self, event):
        if (self.panel.comPanel.list.GetFirstSelected() < 0
                and self.panel.recPanel.list.GetFirstSelected() < 0):
            self.frame.tb.EnableTool(wx.ID_REMOVE, False)
