import pickle
import json
import signal
import threading

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

class Recordings(object):
    """Archive of recordings"""

    def __init__(self, username, password):
        self.recordings = {}
        try:
            self.account = Account(username, password)
        except:
            print 'No connection or wrong credentials'
    
    def saveFile(self):
        f = open('recordings.obj', 'w')
        pickle.dump(self.recordings, f)

    def loadFile(self):
        f = open('recordings.obj', 'r')
        self.recordings = pickle.load(f)

    def download(self, username, password):
        """Download active recordings list and refresh local data
        
        The function first downloads active recordings, then checks which of
        them has a download link.
        """
        a = self.account

        try:
            recs = a.get_recordings()
        except ServerNotFoundError:
            print 'No internet connection or server unreachable'
            return
        if recs == None:
            return

        self.recordings = {}
        for i in recs:
            id_rec = int(i['id_rec'])
            self.recordings[id_rec] = Recording(id_rec,
                    i['title'], i['channel'], i['channel_type'],
                    i['from_time'], i['rec_time'])
        urls = a.get_download_urls()

        for i in urls:
            # Take ID from url and assign it to the object
            m = re.search(r"_(\d+)\.", i)
            id = int(m.group(1))
            try:
                self.recordings[id].url = i
            except:
                print "Recording", id, "not found"

    def delRecording(self, id):
        """Delete a Recording

        Removes the recording both from remote and local.
        """
        del self.recordings[id]
        if not self.account:
            return
        self.account.delete_recording(self.id_rec)
        del recordings.r[id_rec]

    def get_channels(self):
        pass

class Account(object):
    """A vcast account"""

    def __init__(self, username, password):
        """Set up a REST connection to Vcast Server"""

        url = 'http://www.vcast.it/faucetpvr/api/1.0/server_rest.php'
        self.connection = Connection(url)
        self.connection.add_rest_credentials(username, password)
        
        c = self.connection.request_get('/faucetid')
        if c['body'] == 'Access Denied':
            raise Exception('Wrong credentials')
        self.id_usr = json.loads(c['body'])['id_usr']

    def get_channels(self):
        return self.connection.request_get('/channels')

    def get_recordings(self):
        try:
            reply =  self.connection.request_get('/recordings')
            return json.loads(reply['body'])
        except:
            print reply

    def get_download_urls(self):
        """Return the urls of avaible recordings"""
        feed = self.connection.request_get('/feed')['body']
        feed = re.sub(r'\\(.)', r'\1', feed)[13:-3]
        f = feedparser.parse(feed)
        urls = []
        for i in f.entries:
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
    def __init__(self, id_rec, 
            title, channel, channel_type, from_time, rec_time):
        self.id_rec = id_rec
        self.title = title
        self.channel = channel
        self.channel_type = channel_type
        # YYYY-MM-DD HH:MM:SS
        self.from_time = from_time
        self.rec_time = rec_time

        # Calculate to_time field
        a1 = int(from_time[11:13]) + int(rec_time[:2])
        a2 = int(from_time[14:16]) + int(rec_time[3:])
        self.to_time = ""

        self.repeat = "no_repeat"
        self.retention = "3"
        self.has_download = False

class Preferences(object):
    pass
