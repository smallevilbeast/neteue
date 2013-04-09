import sae
import os
import sys

from neteue import wsgi

root = os.path.dirname(__file__)

sys.path.insert(0, os.path.join(root, 'site-packages.zip'))


application = sae.create_wsgi_app(wsgi.application)
