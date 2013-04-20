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
import tarfile
from datetime import datetime
from django.conf import settings
from common.xdg import get_cache_file
from common.threads import threaded
from netpan import NetPan


db_name = settings.DATABASES["default"]["NAME"]
db_user = settings.DATABASES["default"]["USER"]
db_passwd = settings.DATABASES["default"]["PASSWORD"]


netpan_client = NetPan(settings.BAIDU_PAN_USERNAME, settings.BAIDU_PAN_PASSWD)


def get_output_name(dirname="db", ext=".gz"):
    return get_cache_file("%s/%s%s" % (dirname, datetime.now().strftime("%Y%m%d%H%M%S"), ext))

@threaded
def backup_db():
    db_output_file = get_output_name("db", ".gz")
    backup_db_cmd = "mysqldump --opt %s -u %s -p%s | gzip > %s" % (db_name, db_user, 
                                                                   db_passwd, 
                                                                   db_output_file)
    os.system(backup_db_cmd)    
    uploads_output_file = get_output_name("uploads", ".tar.gz")    
    media_root = settings.MEDIA_ROOT
    
    tar_fp = tarfile.open(uploads_output_file,"w|gz")     
    for root, dirs,files in os.walk(media_root):
        for f in files:
            tar_fp.add(os.path.join(root, f))
    tar_fp.close()        
    
    
    if netpan_client.check_login():
        if os.path.isfile(db_output_file):
            netpan_client.upload(db_output_file, "/neteue/db/")
        if os.path.isfile(uploads_output_file):    
            netpan_client.upload(uploads_output_file, "/neteue/uploads/")
