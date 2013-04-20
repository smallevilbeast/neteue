#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2013 Deepin, Inc.
#               2011 ~ 2013 Hou ShaoHui
# 
# Author:     Hou ShaoHui <houshao55@gmail.com>
# Maintainer: Hou ShaoHui <houshao55@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pycurl
import StringIO
import urllib
import time
import random
import string
import hashlib

try:
    import simplejson as json
except ImportError:    
    import json
    
from xdg import get_cache_file    
    
class Curl(object):
    '''
    methods:
    
    GET
    POST
    UPLOAD
    '''
    HEADERS = ['User-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.4 ' \
                   '(KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4',]

    
    def __init__(self, cookie_file=None, headers=HEADERS):
        self.cookie_file = cookie_file
        self.headers = headers
        self.url = ""
    
    def request(self, url, data=None, method="GET", header=None, proxy_host=None, proxy_port=None):
        '''
        open url width get method
        @param url: the url to visit
        @param data: the data to post
        @param header: the http header
        @param proxy_host: the proxy host name
        @param proxy_port: the proxy port
        '''
        if isinstance(url, unicode):
            self.url = str(url)
        else:    
            self.url = url
        
        crl = pycurl.Curl()
        #crl.setopt(pycurl.VERBOSE,1)
        crl.setopt(pycurl.NOSIGNAL, 1)

        # set proxy
        if proxy_host:
            crl.setopt(pycurl.PROXY, proxy_host)
        if proxy_port:
            crl.setopt(pycurl.PROXYPORT, proxy_port)
            
        if self.cookie_file:    
            crl.setopt(pycurl.COOKIEJAR, self.cookie_file)            
            crl.setopt(pycurl.COOKIEFILE, self.cookie_file)            

            
        # set ssl
        crl.setopt(pycurl.SSL_VERIFYPEER, 0)
        crl.setopt(pycurl.SSL_VERIFYHOST, 0)
        crl.setopt(pycurl.SSLVERSION, 3)
         
        crl.setopt(pycurl.CONNECTTIMEOUT, 10)
        crl.setopt(pycurl.TIMEOUT, 300)
        crl.setopt(pycurl.HTTPPROXYTUNNEL, 1)

        headers = self.headers or header
        if headers:
            crl.setopt(pycurl.HTTPHEADER, headers)

        crl.fp = StringIO.StringIO()
            
        if method == "GET" and data:    
            self.url = "%s?%s" % (self.url, urllib.urlencode(data))
            
        elif method == "POST" and data:
            crl.setopt(pycurl.POSTFIELDS, urllib.urlencode(data))  # post data
            
        elif method == "UPLOAD" and data:
            if isinstance(data, dict):
                upload_data = data.items()
            else:
                upload_data = data
            crl.setopt(pycurl.HTTPPOST, upload_data)   # upload file
            
        crl.setopt(pycurl.URL, self.url)
        crl.setopt(crl.WRITEFUNCTION, crl.fp.write)
        try:
            crl.perform()
        except Exception:
            return None
        
        crl.close()
        back = crl.fp.getvalue()
        crl.fp.close()
        return back
    
    
def parser_json(raw):
    try:
        data = json.loads(raw)
    except:    
        try:
            data = eval(raw, type("Dummy", (dict,), dict(__getitem__=lambda s,n: n))())
        except:    
            data = {}
    return data    
    

def timestamp():
    return int(time.time() * 1000)


def get_random_t():
    return random.random()

def radix(n, base=36):
    digits = string.digits + string.lowercase
    def short_div(n, acc=list()):
        q, r = divmod(n, base)
        return [r] + acc if q == 0 else short_div(q, [r] + acc)
    return ''.join(digits[i] for i in short_div(n))

def timechecksum():
    return radix(timestamp())

def quote(s):
    if isinstance(s, unicode):
        s = s.encode("gbk")
    else:    
        s = unicode(s, "utf-8").encode("gbk")
    return urllib.quote(s)    

def unquote(s):
    return urllib.unquote(s)

def get_cookie_file(username):
    return get_cache_file(hashlib.md5(username).hexdigest())

