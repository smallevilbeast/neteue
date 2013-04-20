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


from django.db import models 
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget

from models import (Category, Tag, Article, ArticleTag, Link, BlackList, Subscriber)

class ArticleTagInline(admin.TabularInline):
    model = ArticleTag
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    prepopulated_fields = {"slug" : ("name", )} # 使用name字段来智能填充 Slug 字段
    
class TagAdmin(admin.ModelAdmin):    
    inlines = (ArticleTagInline,)
    prepopulated_fields = {"slug" : ("name", )} # 使用name字段来智能填充 Slug 字段
    
class ArticleAdmin(admin.ModelAdmin):    
    list_display = ("title", "is_always_above", "status", "clicks", "created", "modified")
    prepopulated_fields = {"slug": ("title",)}        
    list_filter = ("status", "created", "modified")
    search_fields = ("title", "content")
    
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget },
        }

    fieldsets = [
        ("文章编辑", {"fields" : ("title", "slug", "content",)}),
        ("日期", {"fields" : ("created", "modified")}),
        ("信息", {"fields" : ("category", "author", "status", "is_always_above", "share")}), 
        ]
    readonly_fields = ("created",)
    
    inlines = (ArticleTagInline,) 
    list_per_page = 10
    ordering = ["-created"]
    
class LinkAdmin(admin.ModelAdmin):
    list_display = ("name", "site")
    
class SubscriberAdmin(admin.ModelAdmin):    
    list_display = ("username", "email_address", "enabled")
        

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(BlackList)
admin.site.register(Subscriber, SubscriberAdmin)
