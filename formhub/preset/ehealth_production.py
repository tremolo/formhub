# this system uses structured settings.py as defined in http://www.slideshare.net/jacobian/the-best-and-worst-of-django

from formhub.settings import *

DEBUG = False  # this setting file will not work on "runserver" -- it needs a real server for static files


ADMINS = [
   ('Adam Thompson', 'adam@ehealthafrica.org'),
]

MANAGERS = ADMINS

# override to set the actual location for the production static and media directories
MEDIA_ROOT = '/var/formhub-media'
STATIC_ROOT = "/srv/formhub-static"
STATICFILES_DIRS = list(STATICFILES_DIRS)
STATICFILES_DIRS.append(os.path.join(PROJECT_ROOT,"eHa/static"))
    # Put strings here, like "/home/html/static" or "C:/www/django/static".

# your actual production settings go here...,.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'formhub',
        'USER': 'formhub_prod',
        'PASSWORD': os.environ['FORMHUB_PROD_PW'],  # the password must be stored in an environment variable
        'HOST': os.environ.get("FORMHUB_DB_SERVER", 'dbserver.yourdomain.org'), # the server name may be in env
        'OPTIONS': {
            'autocommit': True,   # note: this option obsolete starting with django 1.6
        }
    },
    'gis': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'phis',
        'USER': 'staff',
        'PASSWORD': os.environ['PHIS_PW'],  # the password must be stored in an environment variable
        'HOST': 'gisserver.yourdomain.org',
        'OPTIONS': {
            'autocommit': True,
        }
    }
}

#
ALLOWED_HOSTS = ['.eocng.org', '.eocng.org.', 'form.ehealthafrica.org', '.ehealth.org.ng', '']

DATABASE_ROUTERS = ['formhub.preset.dbrouter.GisRouter']

# Local time zone for this installation. Choices can be found here:
TIME_ZONE = 'Africa/Lagos'

EMAIL_HOST = 'smtp.gmail.com'  #The host to use for sending email.

EMAIL_HOST_PASSWORD = os.environ.get("FORMHUB_EMAIL_PASSWORD", "12345678")
#Password to use for the SMTP server defined in EMAIL_HOST.
EMAIL_HOST_USER = 'do.not.reply@ehealthnigeria.org'

EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "do.not.reply@ehealthnigeria.org"

TOUCHFORMS_URL = 'http://localhost:9000/'

MONGO_DATABASE = {
    'HOST': 'localhost',
    'PORT': 27017,
    'NAME': 'formhub',
    'USER': '',
    'PASSWORD': ''
}
# Make this unique, and don't share it with anybody.
SECRET_KEY = 'mlfs33^s1l4xf6a36$0#j%dd*sisfo6HOktYXB9y'
