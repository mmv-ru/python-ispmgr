import urllib, urllib2
from xml.dom import minidom
import logging

class Auth(object):
    """Authorize user against ISPManager instance."""

    def __init__(self, url, username, password,):
        self.url = url
        self.sessid = self.authorize(username, password)

    def authorize(self, username, password):
        params = urllib.urlencode({
            'func': 'auth',
            'out': 'xml',
            'username': username,
            'password': password,
        })
        data = urllib2.urlopen("%s?%s" % (self.url, params))
        out = minidom.parse(data)
        logging.debug('API reply: {}'.format(out.toprettyxml()))
        
        if out.getElementsByTagName('authfail'):
            raise RuntimeError('Authorization error, check your credentials')

        return out.getElementsByTagName('auth')[0].firstChild.nodeValue

    def logout(self):
        params = urllib.urlencode({
            'auth' : self.sessid,
            'func' : 'session.delete',
            'out' : 'xml',
            'elid' : self.sessid,
        })

        data = urllib2.urlopen('%s?%s' % (self.url, params))
        out = minidom.parse(data)

        if out.getElementsByTagName("result") == "OK":
            return True
        else:
            raise RuntimeError('Logout failed!')
