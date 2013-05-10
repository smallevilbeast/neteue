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

from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from django.template import RequestContext
from django.conf import settings

from django.db.models import Count, Max, Min
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from models import Article, Link, Category, Tag
from search import GoogleSearch, Record

DEFAULT_BLOG_THEME = getattr(settings, "BLOG_THEME", "daren")

global_settings={
    'SITE_TITLE':"Neteue",
    'SITE_AUTHOR':"Evilbeast",
    'SITE_DESC':"love it",
    'SITE_SUBTITLE':"Word",
    'SITE_URL':"http://127.0.0.1:8000",
}

PAGE_SIZE = 5
ARCHIVES_PAGE_SIZE = 25
PAGE_ENTRY_DISPLAY_NUM = 6
PAGE_ENTRY_EDGE_NUM = 2

MAX_FONT_SIZE = 20
MIN_FONT_SIZE = 12
MINUS_FONT_SIZE = MAX_FONT_SIZE - MIN_FONT_SIZE


def get_blog_theme(request):
    theme = request.COOKIES.get('blog_theme', DEFAULT_BLOG_THEME)
    if theme not in settings.BLOG_THEMES:
        return DEFAULT_BLOG_THEME
    return theme

def common_response(request):
    tags = Tag.objects.annotate(n_articles=Count("articles"))[:25]
    if tags:
        tag_max_articles = tags.aggregate(Max("n_articles"))['n_articles__max']
        tag_min_articles = tags.aggregate(Min("n_articles"))['n_articles__min']
        for tag in tags:
            if tag_max_articles - tag_min_articles > 0:
                tag.font_size = MIN_FONT_SIZE \
                + MINUS_FONT_SIZE*(tag.n_articles-tag_min_articles)/(tag_max_articles-tag_min_articles)
            else:
                tag.font_size = MINUS_FONT_SIZE
                
    commons = {
        "settings" : global_settings,
        "links"    : Link.objects.all(),
        "tags"     : tags,
        'categories': Category.objects.all(),        
        'populars': Article.completed_objects.order_by('-clicks')[:5],
        }
    return commons

def paginator_response(request, page, p):    
    '''
        p: an instance of Paginator.
    '''
    page = int(page)
    total_pages = p.num_pages
    
    left_continual_max = PAGE_ENTRY_EDGE_NUM + PAGE_ENTRY_DISPLAY_NUM / 2 + 1
    left_continual_range = range(1, page)
    left_edge_range = range(1, PAGE_ENTRY_EDGE_NUM + 1)
    left_range = range(page - PAGE_ENTRY_DISPLAY_NUM / 2, page)
    
    right_continual_min = total_pages - PAGE_ENTRY_DISPLAY_NUM / 2 - 1 \
        if PAGE_ENTRY_DISPLAY_NUM % 2 == 0 else PAGE_ENTRY_DISPLAY_NUM / 2
    right_continual_range = range(page + 1, total_pages + 1)
    right_edge_range = range(total_pages - PAGE_ENTRY_DISPLAY_NUM + 1, total_pages + 1)
    right_range = range(page + 1, page + PAGE_ENTRY_EDGE_NUM + 1)
    
    params = {
        "page" : page,
        "p" : p,
        "left_continual_max" : left_continual_max,
        "left_continual_range" : left_continual_range,
        "left_edge_range" : left_edge_range,
        "left_range" : left_range,
        "right_continual_min" : right_continual_min,
        "right_continual_range" : right_continual_range,
        "right_edge_range" : right_edge_range,
        "right_range" : right_range,
        }
    return params

def index(request, page=1):
    if request.user.is_staff:
        vaild_articles = Article.objects.all()
    else:    
        vaild_articles = Article.completed_objects.all()
    p = Paginator(vaild_articles, PAGE_SIZE)
    
    try:
        current_page = p.page(page)
    except (EmptyPage, InvalidPage):    
        raise Http404
    
    data = {"current_page" : current_page}
    data.update(common_response(request))
    data.update(paginator_response(request, page, p))
    blog_theme = get_blog_theme(request)
    return render_to_response("blog/%s/index.html" % blog_theme, data, 
                              context_instance=RequestContext(request))


def article(request, slug):     
    article = get_object_or_404(Article, slug=slug)
    if not article.is_public and not request.user.is_staff:
        raise Http404
    data = {"article" : article, "comments" : True, "article_tags" : article.tags.all()}
    data.update(common_response(request))
    article.click_once()
    blog_theme = get_blog_theme(request)
    return render_to_response("blog/%s/article.html" % blog_theme, data, 
                              context_instance=RequestContext(request))

def archives(request, page=1):
    if request.user.is_staff:
        vaild_articles = Article.objects.all()
    else:    
        vaild_articles = Article.completed_objects.all()
        
    p = Paginator(vaild_articles, ARCHIVES_PAGE_SIZE)
    
    try:
        current_page = p.page(page)
    except (EmptyPage, InvalidPage):    
        raise Http404
    
    data = {"current_page" : current_page}
    data.update(common_response(request))
    data.update(paginator_response(request, page, p))
    blog_theme = get_blog_theme(request)
    return render_to_response("blog/%s/archives.html" % blog_theme, data)
    
def category(request, slug, page=1):
    category = get_object_or_404(Category, slug=slug)
    
    if request.user.is_staff:
        vaild_articles = Article.objects.filter(category=category)
    else:    
        vaild_articles = Article.completed_objects.filter(category=category)        
    
    p = Paginator(vaild_articles, PAGE_SIZE)
    
    try:
        current_page = p.page(page)
    except EmptyPage:
        raise Http404
    
    data = {"current_page" : current_page, "category" : category}
    data.update(common_response(request))
    data.update(paginator_response(request, page, p))
    blog_theme = get_blog_theme(request)
    return render_to_response("blog/%s/category.html" % blog_theme, data, 
                              context_instance=RequestContext(request))
    

def tag(request, slug, page=1):
    tag = get_object_or_404(Tag, slug=slug)
    
    if request.user.is_staff:
        vaild_articles = Article.objects.filter(tags__slug=slug)
    else:    
        vaild_articles = Article.completed_objects.filter(tags__slug=slug)
        
    p = Paginator(vaild_articles, PAGE_SIZE)        
    
    try:
        current_page = p.page(page)
    except EmptyPage:
        raise Http404
    
    data = {"current_page" : current_page, "tag" : tag}
    data.update(common_response(request))
    if p.num_pages > 1:
        data.update(paginator_response(request, page, p))
    blog_theme = get_blog_theme(request)
    return render_to_response('blog/%s/tag.html' % blog_theme, data)

def about(request):
    data = {"comments" : True}
    data.update(common_response(request))
    blog_theme = get_blog_theme(request)
    return render_to_response("blog/%s/about.html" % blog_theme, data)

def guestbook(request):
    data = {"comments" : True}
    data.update(common_response(request))
    blog_theme = get_blog_theme(request)
    return render_to_response("blog/%s/guestbook.html" % blog_theme, data)

def search(request, page=1):
    page = int(page)
    query = request.GET.get('q', '')
    
    n_per_page = 10
    
    start = (page - 1) * n_per_page + 1
    end = page * n_per_page
    
    count = 0
    p = None
    results = []
    if len(query) > 0:
        search = GoogleSearch(query, page)
        count, results = search()
        if count - start + 1 < n_per_page:
            end = count
            
        result_list = [results[i%n_per_page-1] if start <= i <= end else Record() for i in range(1, count+1)]
        p = Paginator(result_list, n_per_page)
        try:
            current_page = p.page(page)
        except EmptyPage:
            raise Http404
        
    data = {"count" : count, "start" : start, "end" : end,
            "results" : results, "n_per_page" : n_per_page,
            "current_page" : current_page, "p" : p, "query" : query,
            }
    data.update(common_response(request))
    if p and p.num_pages > 1:
        data.update(paginator_response(request, page, p))
    blog_theme = get_blog_theme(request)
    return render_to_response('blog/%s/search.html' % blog_theme, data)
