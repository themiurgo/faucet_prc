import pickle
import json
import simplejson
import signal
from datetime import datetime, timedelta

from restful_lib import Connection
import re
import feedparser


def timeout(func, args=(), kwargs={}, timeout_duration=10, default=None):
    """This function will spawn a thread and run the given function
    using the args, kwargs and return the given default value if the
    timeout_duration is exceeded.
    """ 
    class InterruptableThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = default
        def run(self):
            self.result = func(*args, **kwargs)
    it = InterruptableThread()
    it.start()
    it.join(timeout_duration)
    if it.isAlive():
        return it.result
    else:
        return it.result

class Interface(object):
    """Provides interface for vcast services"""

    def setAccount(self, username, password):
        if not username or not password:
            raise
        try:
            print "Setting account"
            self.account = Account(username, password)
            self.recordings = {}
        except:
            raise

    def saveFile(self):
        d = {}
        d['account'] = self.account
        d['recordings'] = self.recordings
        f = open('save.obj', 'w')
        pickle.dump(d, f)
        f.close()

    def loadFile(self):
        try:
            f = open('save.obj', 'r')
            d = pickle.load(f)
            self.account = d['account']
            self.recordings = d['recordings']
            f.close()
        except:
            raise

    def get_channels(self):
        return self.account.get_channels()

    def getFutureRecordings(self):
        r = {}
        now = datetime.now()
        for k,v in self.recordings.iteritems():
            d = datetime.strptime(v.from_time, "%Y-%m-%d %H:%M:%S")
            if d > now:
                r[k] = v
        return r

    def getPastRecordings(self):
        r = {}
        now = datetime.now()
        for k,v in self.recordings.iteritems():
            d = datetime.strptime(v.from_time, "%Y-%m-%d %H:%M:%S")
            if d <= now:
                r[k] = v
        return r

    def get_recordings(self):
        """Download active recordings list and refresh local data
        
        The function first downloads active recordings, then checks which of
        them has a download link.
        """
        # self.loadFile()
        print "Retrieving recordings..."
        try:
            recs = self.account.get_recordings()
        except:
            print 'No internet connection or server unreachable'
            return self.recordings
        if recs == None:
            return

        self.recordings = {}
        for i in recs:
            id_rec = int(i['id_rec'])
            self.recordings[id_rec] = Recording(id_rec,
                    i['title'], i['channel'], i['channel_type'],
                    i['from_time'], i['rec_time'],i['format'])
        urls = self.account.get_download_urls()

        for i in urls:
            # Take ID from url and assign it to the object
            m = re.search(r"_(\d+)\.", i)
            id = int(m.group(1))
            try:
                self.recordings[id].url = i
            except:
                print "Recording", id, "not found"
        # self.saveFile()
        return self.recordings

    def delRecording(self, id):
        """Delete a Recording

        Removes the recording both from remote and local.
        """
        del self.recordings[id]
        if not self.account:
            return
        self.account.delete_recording(self.id_rec)
        del recordings.r[id_rec]

class Account(object):
    """A vcast account.
    
    This class handles communication with Vcast FAUCET PVR Server
    """

    def __init__(self, username, password):
        """Set up a REST connection to Vcast Server
        
        Returns id_usr user id or raises exception"""
        self.username = username
        self.password = password

        url = 'http://www.vcast.it/faucetpvr/api/1.0/server_rest.php'
        self.connection = Connection(url)
        self.connection.add_rest_credentials(username, password)
        
        c = self.connection.request_get('/faucetid')
        print c
        if c['body'] == 'Access Denied':
            raise Exception('Wrong credentials')
        self.id_usr = simplejson.loads(c['body'])['id_usr']

    def get_channels(self):
        """Return channels.
        
        The function returns channel as a list of dictionaries.
        Each element of the list is a dictionary with two keys,
        - type, whose value is a string that can be "video" or "audio";
        - name, whose value is a string.

        """
        try:
            reply = self.connection.request_get('/channels')
            return simplejson.loads(reply['body'])
        except:
            print reply

    def get_recordings(self):
        """Return recordings.

        The function returns recordings as a list of dictionaries.
        Each element has the following keys whose value is a unicode
        string (type: unicode).
        - id_rec
        - title
        - channel
        - channel_type (can be 'audio' or 'video')
        - format
        - from_time
        - rec_time
        - to_time
        - retention
        - repeat
        - faucetacc (ignore it)

        """
        try:
            reply =  self.connection.request_get('/recordings')
            return simplejson.loads(reply['body'])
        except:
            print reply

    def get_download_urls(self):
        """Return the urls of avaible recordings"""
        feed = self.connection.request_get('/feed')['body']
        feed = re.sub(r'\\(.)', r'\1', feed)[13:-3]
        f = feedparser.parse(feed)
        urls = []
        for i in f.entries:
            print i
            # print i['enclosures'][0]['href']
            urls.append(i['enclosures'][0]['href'])
        return urls

    def new_recording(self, recording):
        """Invia al server una nuova programmazione"""
        pass

    def delete_recording(self, id):
        feed = self.connection.request_get('/delete_recording',
                args={'id_rec':str(id)})

class Recording(object):
    """A recording"""

    def __init__(self, id_rec, title, channel, channel_type, from_time,
            rec_time, format):
        self.id_rec = int(id_rec)
        self.title = title
        self.channel = channel
        self.channel_type = channel_type
        # YYYY-MM-DD HH:MM:SS
        self.from_time = from_time
        self.rec_time = rec_time
        self.format = format

        # Calculate to_time field
        d = datetime.strptime(from_time, "%Y-%m-%d %H:%M:%S")
        h = int(rec_time[:2])
        m = int(rec_time[3:])
        delta = timedelta(hours=h, minutes=m)
        d2 = d+delta
        self.to_time = datetime.strftime(d2, "%Y-%m-%d %H:%M:%S")

        self.repeat = "no_repeat"
        self.retention = "3"
        self.url = None # This change to download url when avaible

i = Interface()
