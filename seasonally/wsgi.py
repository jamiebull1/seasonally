"""
WSGI config for seasonally project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import structlog

log = structlog.get_logger()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seasonally.settings")

try:
    application = get_wsgi_application()
except Exception as e:
    log.error('wsgi.error', {'msg': e})
