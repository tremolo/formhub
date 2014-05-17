### NGINX and uWSGI

follow the guidelines in https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/uwsgi/
and https://uwsgi.readthedocs.org/en/latest/tutorials/Django_and_nginx.html

alter the settings in formhub/preset/production.py to the actual location of your production MEDIA and STATIC roots
alter formhub/nginx.conf to match
    sudo ln -s /opt/formhub/formhub/nginx.conf /etc/nginx/sites-enabled/

uWSGI django.ini file
    sudo ln -s /opt/formhub/formhub/wsgi.ini /etc/uwsgi/vassals/

test using:
    sudo uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data

create the file /etc/init/uwsgi.conf containing:
    # Emperor uWSGI script

    description "uWSGI Emperor"
    start on runlevel [2345]
    stop on runlevel [06]

    exec uwsgi --master --die-on-term --emperor /etc/uwsgi/vassals --uid www-data --gid www-data
start it using
    sudo start uwsgi

install your static files into the directory from which they will be served in production
    ./manage.py collectstatic

