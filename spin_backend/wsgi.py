"""
WSGI config for spin_backend project
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spin_backend.production_settings')

application = get_wsgi_application()
