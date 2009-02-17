import json

from restful_lib import Connection
import re
import feedparser

class Actions(object):
    pass

class Account(object):
    """A vcast account"""

    def __init__(self, username, password):
        url = 'http://www.vcast.it/faucetpvr/api/1.0/server_rest.php'
        self.connection = Connection(url)
        self.connection.add_rest_credentials(username, password)

    def get_channels(self):
        return self.connection.request_get('/channels')

    def get_recordings(self):
        return self.connection.request_get('/recordings')

    def get_feed(self):
        """Return the RSS feed of avaible recordings"""
        feed = self.connection.request_get('/feed')['body']
        feed = re.sub(r'\\(.)', r'\1', feed)[13:-3]
        return feedparser.parse(feed)

    def new_recording(self, recording):
        """Invia al server una nuova programmazione"""
        pass

class Recording(object):
    def __init__(self, title, channel, channel_type, from_time, rec_time):
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

    def save():
        """
        Return id_rec or -1 if error
        """

        pass
        
class Preferences(object):
    pass

a = Account('username','pw')
