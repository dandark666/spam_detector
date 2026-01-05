import os
from django.core.wsgi import get_wsgi_application

# Usar configuración ESPECÍFICA para Render
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spam_detector.render_settings')

application = get_wsgi_application()
