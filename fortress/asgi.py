"""
ASGI config for fortress project
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fortress.production_settings')

application = get_asgi_application()
