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

from django.conf.urls import patterns, url
from feeds import RSSFeed
from sitemap import ArticleSitemap

urlpatterns = patterns(
    "apps.blog.views",
    
    # Index page
    url(r'^$', "index", name="blog_index"),
    url(r'^page/(?P<page>\d+)/$', "index", name="blog_index_pages"),
    
    # Article page
    url(r'article/(?P<slug>[-\w]+)/$', "article", name="blog_article"),
    
    # Category page
    url(r'^category/(?P<slug>\w+)/$', 'category', name='blog_category'),
    url(r'^category/(?P<slug>\w+)/page/(?P<page>\d+)/$', 'category', name='blog_category_pages'),
    
    # # Tag
    url(r'^tag/(?P<slug>[-\w]+)/$', 'tag', name='blog_tag'),
    url(r'^tag/(?P<slug>[-\w]+)/page/(?P<page>\d+)/$', 'tag', name='blog_tag_pages'),
    
    # About
    url(r'^about/$', 'about', name='blog_about'),

    # Message
    url(r'^guestbook/$', "guestbook", name="blog_guestbook"),
    
    # Search
    url(r'^search/$', 'search', name='blog_search'),
    url(r'^search/page/(?P<page>\d+)/$', 'search', name='blog_search_pages'),
    
    # archives
    url(r'^archives/$', 'archives', name="blog_archives"),
    url(r'^archives/page/(?P<page>\d+)/$', "archives", name="blog_archives_pages"),
    
    # # Subscriber
    # url(r'^subscriber/add/$', 'subscriber', name='blog_subscriber'),
    # # Unsubscribe
    # url(r'^subscribe/cancel/$', 'unsubscriber', name='blog_unsubscriber')
)


# rss
urlpatterns += patterns('',
    url(r'^feed/$', RSSFeed(), name='blog_feed'),
)

# Sitemap
sitemaps = {  
    'article': ArticleSitemap,       
}
urlpatterns += patterns('',
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}), 
)