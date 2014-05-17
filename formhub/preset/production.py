# this system uses structured settings.py as defined in http://www.slideshare.net/jacobian/the-best-and-worst-of-django

try:
    from ..settings import *
except ImportError:
    import sys, django
    django.utils.six.reraise(RuntimeError, *sys.exc_info()[1:])  # use RuntimeError to extend the traceback
except:
    raise

DEBUG = False  # this setting file will not work on "runserver" -- it needs a server for static files

ADMINS = (
    ('Adam', 'adam@ehealthafrica.org'),
)

MANAGERS = ADMINS

# override to set the actual location for the production static and media directories
MEDIA_ROOT = '/var/formhub-media'
STATIC_ROOT = "/srv/formhub-static"

# your actual production settings go here...,.
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'phis',
        'USER': 'phis',
        'PASSWORD': 'nopolio4u', # os.environ['PHIS_PW'],  # the password must be stored in an environment variable
        'HOST': 'nomads.eocng.org',
        'OPTIONS': {
            'autocommit': True,
        }
    }
}

#
ALLOWED_HOSTS = ['formhub.eocng.org', 'forms.ehealthafrica.org',
		'forms.ehealth.org.ng']

#DATABASE_ROUTERS = ['formhub.preset.dbrouter.GisRouter']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Africa/Lagos'

BROKER_URL = 'amqp://formhub:12345678@localhost:5672/formhub_vhost'

EMAIL_HOST = 'smtp.gmail.com'  #The host to use for sending email.

EMAIL_HOST_PASSWORD = "donotreply12345"  #os.environ.get("FORMHUB_EMAIL_PASSWORD", "12345678")
#Password to use for the SMTP server defined in EMAIL_HOST.
EMAIL_HOST_USER = 'do.not.reply@ehealthnigeria.org'

EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "do.not.reply@ehealthafrica.org"

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

TESTING_MODE = False

ENKETO_URL = 'https://enketo.org/'
ENKETO_API_TOKEN = 'mo4ao9nrr5a2x1or'
