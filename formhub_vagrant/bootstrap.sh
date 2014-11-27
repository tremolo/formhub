#!/usr/bin/env bash
SERVER_BASEDIR=/opt
FORMHUB_VIRTUALENV=/opt/virtual_environments/formhub
FORMHUB_GIT_REPO="https://github.com/tremolo/formhub.git"
FORMHUB_GIT_BRANCH="feature/server_setup"
FORMHUB_BASE=$SERVER_BASEDIR/formhub
# DB user name for formhub
POSTGRES_USER=formhub
# DB name for formhub
POSTGRES_DB=formhubdjangodb
# #  the host of the postgres server
POSTGRES_HOST=localhost

FORMHUB_SETTINGS=ehealth_test

# install base packages with package manager
apt-get update
apt-get -y upgrade

locale-gen UTF-8

apt-get install -y gfortran libatlas-base-dev libjpeg-dev zlib1g-dev rsync pwgen
apt-get -y install nginx uwsgi python-virtualenv fabric git libxml2 libxml2-dev libxslt1.1 libxslt1-dev python-dev cython
apt-get install -y mongodb

apt-get install  -y postgresql postgresql-contrib
# for the psycog2 module
 apt-get install  -y postgresql-server-dev-9.3
apt-get install -y python-psycopg2 
apt-get install -y celeryd

# java needed for pyxform validation
#apt-get  install -y openjdk-7-jre-headless

# now we can generate our postgres password
POSTGRES_PASSWORD=`pwgen -c -n -1 12`


# create the virtualenv environment and install the requirements

if [ ! -f $FORMHUB_VIRTUALENV ]; then
    virtualenv  $FORMHUB_VIRTUALENV
fi

# checkout sources and install python dependencies
source $FORMHUB_VIRTUALENV/bin/activate
git clone -b $FORMHUB_GIT_BRANCH $FORMHUB_GIT_REPO $FORMHUB_BASE
pip install -r $FORMHUB_BASE/requirements.pip

# add the postgres driver installed by apt-get to the virtualenv
#rsync -av /usr/lib/python2.7/dist-packages/psycopg2 $FORMHUB_VIRTUALENV/lib/python2.7/site-packages/

# Init the DB
POSTGRES_CLEARDB="DROP DATABASE IF EXISTS $POSTGRES_DB;"
POSTGRES_CLEARUSER="DROP USER IF EXISTS $POSTGRES_USER;" 
POSTGRES_INITDB="CREATE USER $POSTGRES_USER WITH  PASSWORD '$POSTGRES_PASSWORD';"
# only for testing, django test runner needs permission to create test database
POSTGRES_TESTUSER_PERMISSION="ALTER USER $POSTGRES_USER  CREATEDB;"


# just start postgres to update the base settings and stop it again
/etc/init.d/postgresql start && \
   sudo -u postgres psql --command "$POSTGRES_CLEARDB" &&  \
   sudo -u postgres psql --command "$POSTGRES_CLEARUSER" &&  \
   sudo -u postgres psql --command "$POSTGRES_INITDB" &&  \
   sudo -u postgres psql --command "$POSTGRES_TESTUSER_PERMISSION" &&  \
   sudo -u postgres createdb -O $POSTGRES_USER $POSTGRES_DB && \
wait 1s
#/etc/init.d/postgresql stop

# update django config
sed -i "s/POSTGRES_DB/$POSTGRES_DB/g;s/POSTGRES_USER/$POSTGRES_USER/g;s/POSTGRES_PASSWORD/$POSTGRES_PASSWORD/g;s/POSTGRES_HOST/$POSTGRES_HOST/g" $FORMHUB_BASE/formhub/preset/$FORMHUB_SETTINGS.py

cd $FORMHUB_BASE

echo "fetching submodule data"
git submodule init
git submodule update
echo "installing fixtures"
$FORMHUB_VIRTUALENV/bin/python manage.py syncdb --noinput --settings=formhub.preset.$FORMHUB_SETTINGS
$FORMHUB_VIRTUALENV/bin/python manage.py migrate --noinput --settings=formhub.preset.$FORMHUB_SETTINGS
$FORMHUB_VIRTUALENV/bin/python manage.py collectstatic --clear --noinput --settings=formhub.preset.$FORMHUB_SETTINGS


echo "ok, now login with"
echo "$ vagrant ssh "
echo "in the virtual machine activate the environment"
echo "$ source $FORMHUB_VIRTUALENV/bin/activate"
echo "$ cd $FORMHUB_BASE"
echo
echo "and run the tests:"
echo "$ python manage.py test --noinput --settings=formhub.preset.$FORMHUB_SETTINGS api main odk_logger odk_viewer restservice sms_support staff stats"
echo
echo "or run the server with "
echo "$ python manage.py runserver --settings=formhub.preset.$FORMHUB_SETTINGS"
