import urllib
import urllib2
from xml.dom import minidom
import logging

class API(object):
    """Common class for other, specific, classes."""

    def process_api(self, url, params):
        api_request = ("%s?%s" % (url, urllib.urlencode(params)))
        logging.debug('api_request: {}'.format(api_request))
        out = minidom.parse(urllib2.urlopen(api_request))
        logging.debug('API reply: {}'.format(out.toprettyxml()))
        if out.getElementsByTagName('error'):
            raise RuntimeError('Error:{} {}'.format(out.getElementsByTagName('error')[0].attributes["code"].value,
                                                    out.getElementsByTagName('error')[0].firstChild.nodeValue))
        return out
