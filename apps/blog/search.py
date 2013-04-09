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

import urllib2, urllib
import json

from django.conf import settings

class callable(object):
    def __call__(self):
        raise NotImplementedError

class Record(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

class SearchModel(callable):
    def __init__(self, q):
        self._q = q
        
class GoogleSearch(SearchModel):
    key = settings.GOOGLE_SIMPLE_API_KEY
    cx = settings.GOOGLE_SEARCH_ENGINE_UNIQUE_ID
    
    url = settings.GOOGLE_CUSTOM_SEARCH_ENDPOINT
    
    def __init__(self, q, page=1):
        SearchModel.__init__(self, q)
        self._page = page
    
    def _get_data(self):
        start = (self._page - 1) * 10 + 1 
        
        data = {'q': self._q.encode("utf-8")}
        str = urllib.urlencode(data)
        
        abs_url = "%s?key=%s&cx=%s&%s&start=%d" % (self.url, self.key, self.cx, str, start)
        
        data = urllib2.urlopen(abs_url)
        
        resultContent = data.read()
        #print resultContent
        return resultContent
    
    def _get_json(self):
        if getattr(self, '_json', None) is None:
            self._json = json.loads(self._get_data())
        return self._json

    def _get_count(self):
        _json = self._get_json()
        return int(_json['queries']['request'][0]['totalResults'])
    
    def _get_result_list(self):
        _json = self._get_json()
        return _json['items']
    
    def __call__(self):
        records = []
        try:
            results =  self._get_result_list()
            for r in results:
                record = Record(title=r['title'], 
                                htmlSnippet=r['htmlSnippet'], 
                                link=r['link'])
                records.append(record)
        except KeyError:
            pass
            # print KeyError.message
        return self._get_count(), records
