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

import os
from django.utils.text import Truncator

root_dir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]

def get_path(*subpath_elements, **kwargs):
    # check_exists = kwargs.get("check_exists", True)
    subpath = os.path.join(*subpath_elements)
    path = os.path.join(root_dir, subpath)
    return path
    
def truncatewords(value, length, html=True):  
    return Truncator(value).words(length, html=html, truncate=' ...')
