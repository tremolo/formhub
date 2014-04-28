# This system uses structured settings.py as defined in the 
# second from last slide in this presentation:
# http://www.slideshare.net/jacobian/the-best-and-worst-of-django

# The basic idea is that a file like this, which is referenced when
# the django app runs, imports from ../settings.py, and over-rides
# and value there with a value specified here

# This file is checked into source control as an example, but 
# your actual production settings, which contain database passwords
# and 3rd party private keys, etc., should perhaps be omitted using
# .gitignore

from formhub.settings import *

# in this example we are supplementing the django database
# definition found in the ../settings.py file with a password
# (normally we wouldn't check this into source control, but this
#  is here just for illustration, as an example of what's possible)

DATABASES['default']['PASSWORD'] = 'foo'
# an alternative to hard-coding the password string
# is to define the db password as an environment variable:
#DATABASES['default']['PASSWORD'] = os.environ['FORMHUB_DB_PWD']

# examples of other over-rides you could do here:

DATABASE_ROUTERS = [] # turn off second database

# Make a unique unique key just for testing, and don't share it with anybody.
SECRET_KEY = 'mlfs33^s1l4xf6a36$0#j%dd*sisfoi&)&4s-v=91#^l01v)*j'
