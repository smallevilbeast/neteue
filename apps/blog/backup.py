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
from netpan import NetPan, run_cmd


db_name = settings.DATABASES["default"]["NAME"]
db_user = settings.DATABASES["default"]["USER"]
db_passwd = settings.DATABASES["default"]["PASSWORD"]


netpan_client = NetPan(settings.BAIDU_PAN_USERNAME, settings.BAIDU_PAN_PASSWD)


def get_output_name(prefix="db", ext=".gz"):
    base_name = "%s%s%s" % (prefix, datetime.now().strftime("%Y%m%d"), ext)
    full_path = get_cache_file(base_name)
    return base_name, full_path

@threaded
def backup_db():
    db_basename, db_localpath = get_output_name("db", ".gz")
    backup_db_cmd = "mysqldump --opt %s -u %s -p%s | gzip > %s" % (db_name, db_user, 
                                                                   db_passwd, 
                                                                   db_localpath)
    os.system(backup_db_cmd)    
    images_basename, images_localpath = get_output_name("images", ".tar.gz")    
    media_root = settings.MEDIA_ROOT
    
    tar_fp = tarfile.open(images_localpath, "w|gz")     
    for root, dirs,files in os.walk(media_root):
        for f in files:
            tar_fp.add(os.path.join(root, f))
    tar_fp.close()        
    
    if netpan_client.check_login():
        if os.path.isfile(db_localpath):
            print "start backup db...."            
            netpan_client.remove("/neteue/%s" % db_basename)
            netpan_client.upload(db_localpath, "/neteue/")
            print "end backup db...."
        if os.path.isfile(images_localpath):    
            print "start backup staticfiles...."
            netpan_client.remove("/neteue/%s" % images_basename)
            netpan_client.upload(images_localpath, "/neteue/")
            print "end backup staticfiles...."

def run_netpan():            
    run_cmd(settings.BAIDU_PAN_USERNAME, settings.BAIDU_PAN_PASSWD)    
