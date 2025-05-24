import os
import sys

# WSGI

sys.path.insert(0, "/home1/capitaln/dashboard.capitalnestgroup.com")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "capitalnest.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
