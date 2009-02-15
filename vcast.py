from restful_lib import Connection
import re
import feedparser

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

class Preferences(object):
    pass

a = Account('username','pw')
