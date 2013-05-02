#! /usr/bin/env python
# -*- coding: utf-8 -*-


import re
import os
import urllib2

from urlparse import urljoin


def get_images(url):
    content = urllib2.urlopen(url).read()
    head = "/".join(url.split("/")[:-1])
    image_pattern = re.compile(r'url\((.*?)\)')
    image_list = image_pattern.findall(content)
    image_result = set([image.replace('"', "").replace("'", "") for image in image_list])
    results = [os.path.join(head, image) for image in image_result if not image.startswith("http")]
    for i in results:
        print "[info] --> Downloading '%s'" % (i.split("/")[-1])
        os.system("wget %s" % i)

    
    
get_images("https://tower.im/assets/application-e29dbf5d5173307cca4468cdf9b9436a.css")    
    
    
    
    
