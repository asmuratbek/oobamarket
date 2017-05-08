#!/bin/bash

### Define script variables
### =====================================================================================================================

NAME="ooba"                                         # Name of the application
VIRTUALENV="/var/www/ooba/.env"                         # Path to virtualenv
DJANGODIR="/var/www/ooba"                               # Django Project Directory
USER=root                                            # the user to run as
GROUP=root                                           # the group to run as
NUM_WORKERS=3                                                   # No. of worker processes Gunicorn should spawn
DJANGO_SETTINGS_MODULE=config.settings.production               # Settings file that Gunicorn should use
DJANGO_WSGI_MODULE=config.wsgi                                  # WSGI module name


### Activate virtualenv and create environment variables
### =====================================================================================================================

echo "Starting $NAME as `whoami`"
# Activate the virtual environment
cd $VIRTUALENV
source bin/activate
cd $DJANGODIR
# Defining the Environment Variables
export DJANGO_SECRET_KEY='CHANGEME!!!8%ylffu)6j0ogx9a6*$ck2uuw3-7zbm2_j)#0%v=h0ax6rdkw0'
export DATABASE_URL='postgres:///market'
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH


### Start Gunicorn
### =====================================================================================================================

exec gunicorn ${DJANGO_WSGI_MODULE}:application \
        --name $NAME \
        --workers $NUM_WORKERS \
        --user=$USER --group=$GROUP \
        --log-level=debug \
        --bind=188.120.230.176:8000
