"""
ASGI config for spin_backend project
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spin_backend.production_settings')

application = get_asgi_application()
