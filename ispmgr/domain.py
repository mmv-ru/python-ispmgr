import json
import api
from xml.dom import minidom

class Domain(api.API):

    def __init__(self, auth_handler):
        self.url = auth_handler.url
        self.sessid = auth_handler.sessid
        self.func = 'domain.record'
        self.out = 'xml'
        self._clear_params()

    def _clear_params(self):
        try:
            self.params.clear()
        except (NameError,AttributeError):
            pass
        self.params = {
            'auth' : self.sessid,
            'out'  : 'xml',
            'func' : self.func,
        }

    def domains(self, domain=None):
        """List all www domains. If domains is used, list details about this one."""
        self._clear_params()
        if domain:
            self.params['elid'] = domain
        else:
            self.params['func'] = 'domain'
        data = self.process_api(self.url, self.params)
        out = minidom.parse(data)
        print out.toprettyxml()
        if out.getElementsByTagName('error'):
            raise RuntimeError('Error:{} {}'.format(out.getElementsByTagName('error')[0].attributes["code"].value,
                                                    out.getElementsByTagName('error')[0].firstChild.nodeValue))
        try:
            return list(map(lambda x: dict(map(lambda y: (y, x.getElementsByTagName(y)[0].firstChild.nodeValue),
                           ['name', 'dispname'])),
                           out.getElementsByTagName('elem')
                           ))
        except KeyError:
            return out

    def records(self, domain):
        """List all www domains. If domains is used, list details about this one."""
        self._clear_params()
        self.params['func'] = 'domain.sublist'
        self.params['elid'] = domain
        data = self.process_api(self.url, self.params)
        out = minidom.parse(data)
        print out.toprettyxml()
        if out.getElementsByTagName('error'):
            raise RuntimeError('Error:{} {}'.format(out.getElementsByTagName('error')[0].attributes["code"].value,
                                                    out.getElementsByTagName('error')[0].firstChild.nodeValue))
        try:
            return list(map(lambda x: dict(map(lambda y: (y, x.getElementsByTagName(y)[0].firstChild.nodeValue),
                           ['key', 'name', 'type', 'addr'])),
                           out.getElementsByTagName('elem')
                           ))
        except KeyError:
            return out

    def add(self, domain,  owner, admin, ip, **kwargs):
        """Add a new wwwdomain to configuration. If a DNS server is configurated, API adds
        domain there too."""
        self._clear_params()
        self.params['sok']    = 'yes'
        self.params['domain'] = domain
        self.params['owner']  = owner
        self.params['admin']  = admin
        self.params['ip']     = ip
        for key in kwargs:
            self.params[key] = kwargs[key]

        data = self.process_api(self.url, self.params)
        out = json.load(data)
        return out

    def delete(self, domain, **kwatgs):
        """Delete one or list of domains."""
        self._clear_params()
        self.params['func'] = 'wwwdomain.delete'

        if type(domain) is list:
            self.params['elid'] = ', '.join(domain)
        else:
            self.params['elid'] = domain

        data = self.process_api(self.url, self.params)
        out = json.load(data)
        return out

    def delete_confirm(self, domain, **kwargs):
        raise NotImplementedError

    def plain(self, domain, **kwargs):
        """View apache/nginx configs"""
        self._clear_params()
        self.params['func'] = 'wwwdomain.plain'
        self.params['elid'] = domain

        data = self.process_api(self.url, self.params)
        out = json.load(data)
        return out

    def enable(self, domain, **kwargs):
        """Enable domain."""
        raise NotImplementedError

    def disable(self, domain, **kwargs):
        """Disable domain."""
        raise NotImplementedError
