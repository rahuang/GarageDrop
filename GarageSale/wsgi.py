"""
WSGI config for GarageSale project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GarageSale.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

try:    # It's okay if this Cling thingy doesn't exist, because if it doesn't exist, it's not running on Heroku.
    from dj_static import Cling     # (try... except added by yamcat)
    application = Cling(get_wsgi_application())
except ImportError:
    pass
    