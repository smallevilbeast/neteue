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

from django.contrib.syndication.views import Feed
from django.conf import settings
from models import Article
from common import truncatewords

class RSSFeed(Feed):
    title = getattr(settings, "SITE_TITLE", u"Neteue Site")
    description = getattr(settings, "SITE_DESCRIPTION", "Neteue blog")
    link = "/"
    
    def items(self):
        return Article.completed_objects.all().order_by("-created")[:10]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return truncatewords(item.abstract, 25)
