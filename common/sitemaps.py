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

from django.contrib.sitemaps import ping_google
from django.conf import settings

def ping_all_search_engines(sitemap_url=settings.SITE+'/sitemap.xml'):
    
    SEARCH_ENGINE_PING_URLS = (
        ('google', 'http://www.google.com/webmasters/tools/ping'),
        ('yahoo', 'http://search.yahooapis.com/SiteExplorerService/V1/ping'),
        ('ask', 'http://submissions.ask.com/ping'),
        ('live', 'http://webmaster.live.com/ping.aspx'),
    )
    successfully_pinged = []
    for (site, url) in SEARCH_ENGINE_PING_URLS:
        try:
            ping_google(sitemap_url=sitemap_url, ping_url=url)
            pinged = True
        except:
            pinged = False
        if pinged:
            successfully_pinged.append(site)
    return successfully_pinged
