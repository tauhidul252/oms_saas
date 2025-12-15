"""
WSGI config for oms_saas project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oms_saas.settings')

application = get_wsgi_application()
