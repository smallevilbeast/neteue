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
from django.db.models import permalink
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from managers import (CompletedArticleManager, EnabledSubscriberManager)

from django.db.models.signals import post_save
from django.dispatch import receiver
# from common.sitemaps import ping_all_search_engines
from django.contrib.sitemaps import ping_google


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="分类名称")
    slug = models.SlugField(unique=True)
    order = models.IntegerField(blank=True, null=True, verbose_name="顺序")
    
    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类"
        ordering = ['order']
        
    def __unicode__(self):    
        return self.name
    
    @permalink
    def get_absolute_url(self):
        return ("blog_category", None, {"slug" : self.slug})
    
    def save(self):
        if self.order is None:
            cates = Category.objects.all()
            if cates:
                max_order = cates.order_by('-order')[0]
                self.order = max_order.order + 1
            else:    
                self.order = 1
                
        super(Category, self).save()        
        

class Tag(models.Model):        
    name = models.CharField(max_length=50, unique=True, verbose_name="标签名称")
    slug = models.SlugField(unique=True)
    
    # through: 指定ArticleTag model来管理多对对关系.
    articles = models.ManyToManyField("Article", through="ArticleTag", verbose_name="文章")
    
    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"
        # ordering = ['?'] # ? 表示随机排序

        
    def __unicode__(self):        
        return self.name
    
    @permalink
    def get_absolute_url(self):
        return ("blog_tag", None, {"slug" : self.slug})
    
    
class Article(models.Model):    
    
    STATUS_CHOICE = (
        (1, "编辑"),
        (2, "完成"),
        (3, "失效"),
        )
    
    title = models.CharField(max_length=100, verbose_name="标题")
    slug = models.SlugField(max_length=100, unique=True)
    content = models.TextField(verbose_name="内容")
    # markdown = models.TextField(verbose_name=u'内容')
    # content = models.TextField(blank=True, editable=False)
    status = models.IntegerField(choices=STATUS_CHOICE, default=1, verbose_name="状态")
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    modified = models.DateTimeField(default=timezone.now, verbose_name="修改时间")
    is_always_above = models.BooleanField(default=False, verbose_name="置顶")
    share = models.BooleanField(default=False, verbose_name="同步到网盘")
    clicks = models.IntegerField(default=0, editable=False, verbose_name="点击次数")
    
    category = models.ForeignKey(Category, verbose_name="分类")
    author = models.ForeignKey(User, verbose_name="作者")
    
    tags = models.ManyToManyField(Tag, through="ArticleTag", verbose_name="标签")
    
    # Manager
    objects = models.Manager()
    completed_objects = CompletedArticleManager() # 过滤已完成的文章

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章"
        ordering =  ['-is_always_above', '-created']
        
    def click_once(self):    
        self.clicks += 1
        super(Article, self).save(update_fields=['clicks'])
        
    def __unicode__(self):    
        return self.title
    
    @property
    def is_public(self):
        return self.status == 2
    
    @permalink
    def get_absolute_url(self):
        return ("blog_article", None, {"slug": self.slug})
    
    def __getattr__(self, name):
        if name == "abstract":
            return self.content
        return super(Article, self).__getattr__(name)
    
    
class ArticleTag(models.Model):    
    article = models.ForeignKey(Article)
    tag = models.ForeignKey(Tag)
    
    class Meta:
        verbose_name = "文章标签"
        verbose_name_plural = "文章标签"
    
    def __unicode__(self):    
        return unicode(self.tag)
    
class Link(models.Model):
    name = models.CharField(max_length=50, verbose_name='链接名')
    site = models.URLField(verbose_name='链接地址')
    
    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = '友情链接'
        ordering = ["name",]
        
    def __unicode__(self):
        return self.name
    
class BlackList(models.Model):
    ip_address = models.IPAddressField(verbose_name='IP地址')
    
    class Meta:
        verbose_name = '黑名单'
        verbose_name_plural = '黑名单'
        
    def __unicode__(self):
        return self.ip_address
    
    
class Subscriber(models.Model):
    username = models.CharField(max_length=50, verbose_name="订阅用户")
    email_address = models.EmailField(verbose_name="邮箱地址")
    subscribe_time = models.DateTimeField(auto_now_add=True, verbose_name='订阅时间')
    enabled = models.BooleanField(default=True, verbose_name='是否开启')
    
    # Manager
    objects = models.Manager()
    enabled_objects = EnabledSubscriberManager() # 过滤所有订约的用户
    
    class Meta:
        verbose_name = '订阅用户'
        verbose_name_plural = '订阅用户'
        
    def __unicode__(self):
        return self.username

class ArticleSubscriber(models.Model):
    article = models.ForeignKey(Article)
    subscriber = models.ForeignKey(Subscriber)
    
    class Meta:
        verbose_name = "文章订阅信息"
        verbose_name_plural = "文章订阅信息"
        
    def __unicode__(self):
        return unicode(self.article)
    
@receiver(post_save, sender=Article, dispatch_uid="ping_google")
def ping_search_engines(sender, instance, **kwargs):
    article = instance
    
    if not settings.DEBUG and article.status == 2:
        try:    
            ping_google()
        except:    
            pass
        

@receiver(post_save, sender=Article, dispatch_uid="sync_to_pan")
def sync_to_pan(sender, instance, **kwargs):
    article = instance
    
    if article.share:
        article.share = False
        article.save(update_fields=["share"])
        from backup import backup_db
        backup_db()
