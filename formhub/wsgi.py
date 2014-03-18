import os

# in real production, DJANGO_SETTINGS_MODULE must be defined externally
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "formhub.preset.staging")

# This application object is used by the development server
# as well as any WSGI server configured to use this file.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
