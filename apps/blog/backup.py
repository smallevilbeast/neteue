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


def get_output_name(dirname="db", ext=".gz"):
    base_name = "%s%s" % (datetime.now().strftime("%Y%m%d"), ext)
    full_path = get_cache_file("%s/%s" % (dirname, base_name))
    return base_name, full_path

@threaded
def backup_db():
    db_basename, db_localpath = get_output_name("db", ".gz")
    backup_db_cmd = "mysqldump --opt %s -u %s -p%s | gzip > %s" % (db_name, db_user, 
                                                                   db_passwd, 
                                                                   db_localpath)
    os.system(backup_db_cmd)    
    staticfile_basename, staticfile_localpath = get_output_name("uploads", ".tar.gz")    
    media_root = settings.MEDIA_ROOT
    
    tar_fp = tarfile.open(staticfile_localpath,"w|gz")     
    for root, dirs,files in os.walk(media_root):
        for f in files:
            tar_fp.add(os.path.join(root, f))
    tar_fp.close()        
    
    
    if netpan_client.check_login():
        if os.path.isfile(db_localpath):
            netpan_client.remove("/neteue/db/%s" % db_basename)
            print "start backup db...."
            netpan_client.upload(db_localpath, "/neteue/db/")
            print "end backup db...."
        if os.path.isfile(staticfile_localpath):    
            print "start backup staticfiles...."
            netpan_client.remove("/neteue/uploads/%s" % staticfile_basename)
            netpan_client.upload(staticfile_localpath, "/neteue/uploads/")
            print "end backup staticfiles...."

def run_netpan():            
    run_cmd(settings.BAIDU_PAN_USERNAME, settings.BAIDU_PAN_PASSWD)    
