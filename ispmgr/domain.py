#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

    def domains(self):
        """List all domains."""
        self._clear_params()
        self.params['func'] = 'domain'
        out = self.process_api(self.url, self.params)
        try:
            return list(map(lambda x: dict(map(lambda y: (y, x.getElementsByTagName(y)[0].firstChild.nodeValue),
                           ['name', 'dispname'])),
                           out.getElementsByTagName('elem')
                           ))
        except KeyError:
            return out

    def records(self, domain):
        """List all records for domains."""
        self._clear_params()
        self.params['func'] = 'domain.sublist'
        self.params['elid'] = domain
        out = self.process_api(self.url, self.params)
        try:
            return list(map(lambda x: dict(map(lambda k: (k, x.getElementsByTagName(k)[0].firstChild.nodeValue),
                           filter(lambda v: x.getElementsByTagName(v) , ['key', 'name', 'type', 'addr', 'prio', 'wght', 'port']))),
                           out.getElementsByTagName('elem')
                           ))
        except KeyError:
            logging.error('parsing API reply: {}'.format(out.toprettyxml()))
            return out

    def record_edit(self, domain, key, **kwargs):
        """Edit domain record.
        name - Имя.
        sdtype - Тип. 
          Возможные значения :
                A - A (адрес Internet v4)
                AAAA - AAAA (адрес Internet v6)
                CNAME - CNAME (каноническое имя)
                DNAME - DNAME (делегированное имя)
                NS - NS (сервер имён)
                MX - MX (почтовый сервер)
                TXT - TXT (текстовая запись)
                SRV - SRV (сетевой сервис)
                PTR - PTR (реверсная запись) 

        При выбранном значении MX разрешается использовать параметры: 'prio' и запрещается использовать параметры: 'wght','port'
        При выбранном значении SRV разрешается использовать параметры: 'prio','wght','port'
        При выбранном значении A запрещается использовать параметры: 'prio','wght','port'
        При выбранном значении AAAA запрещается использовать параметры: 'prio','wght','port'
        При выбранном значении CNAME запрещается использовать параметры: 'prio','wght','port'
        При выбранном значении DNAME запрещается использовать параметры: 'prio','wght','port'
        При выбранном значении NS запрещается использовать параметры: 'prio','wght','port'
        При выбранном значении TXT запрещается использовать параметры: 'prio','wght','port'
        При выбранном значении PTR запрещается использовать параметры: 'prio','wght','port'

        addr - Адрес.
        prio - Приоритет.
        wght - Условный вес SRV-записи.
        port - Порт.         """
        
        self._clear_params()
        self.params['sok']  = 'yes'
        self.params['func'] = 'domain.sublist.edit'
        self.params['plid'] = domain
        self.params['elid'] = key
        for key in kwargs:
            self.params[key] = kwargs[key]
        
        out = self.process_api(self.url, self.params)
        try:
            return list(map(lambda x: dict(map(lambda k: (k, x.getElementsByTagName(k)[0].firstChild.nodeValue),
                           filter(lambda v: x.getElementsByTagName(v) , ['key', 'name', 'type', 'addr', 'prio', 'wght', 'port']))),
                           out.getElementsByTagName('elem')
                           ))
        except KeyError:
            logging.error('parsing API reply: {}'.format(out.toprettyxml()))
            return out


    #def add(self, domain,  owner, admin, ip, **kwargs):
        #"""Add a new wwwdomain to configuration. If a DNS server is configurated, API adds
        #domain there too."""
        #self._clear_params()
        #self.params['sok']    = 'yes'
        #self.params['domain'] = domain
        #self.params['owner']  = owner
        #self.params['admin']  = admin
        #self.params['ip']     = ip
        #for key in kwargs:
            #self.params[key] = kwargs[key]

        #data = self.process_api(self.url, self.params)
        #out = json.load(data)
        #return out

    #def delete(self, domain, **kwatgs):
        #"""Delete one or list of domains."""
        #self._clear_params()
        #self.params['func'] = 'wwwdomain.delete'

        #if type(domain) is list:
            #self.params['elid'] = ', '.join(domain)
        #else:
            #self.params['elid'] = domain

        #data = self.process_api(self.url, self.params)
        #out = json.load(data)
        #return out

    #def delete_confirm(self, domain, **kwargs):
        #raise NotImplementedError

    #def enable(self, domain, **kwargs):
        #"""Enable domain."""
        #raise NotImplementedError

    #def disable(self, domain, **kwargs):
        #"""Disable domain."""
        #raise NotImplementedError
