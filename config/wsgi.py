"""
WSGI config for config project.
"""

import os
from django.core.wsgi import get_wsgi_application

# Indicamos donde debe buscar las configuraciones del proyecto el servidor web
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
