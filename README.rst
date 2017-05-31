Ooba Market
===========

market

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django


:License: MIT
Install project
--------

1. Download the project

 $ git clone https://<your_username>@bitbucket.org/monokbaev/ooba.git

2. Create virtual enviroment(python-3.5)

 $ sudo apt-get install -y python3-pip
   this command install python-3 on your system
 $ sudo apt-get install build-essential libssl-dev libffi-dev python-dev
   install dependencies
 $ sudo apt-get install -y python3-venv
   install library for virtual enviroment
 $ pyvenv my_env
   create virtual enviroment for project
3. Activate your enviroment, open /requirements/ dir and install all required libraries
  $ pip install -r local.txt

  $ pip install -r test.txt
4. If you don`t have elasticsearch in your system, install it.
  $ wget https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/deb/elasticsearch/2.3.1/elasticsearch-2.3.1.deb
    download elasticsearch
  $ sudo dpkg -i elasticsearch-2.3.1.deb
    install command
  $ sudo systemctl enable elasticsearch.service
    to make sure elasticsearch starts and stops automatically with the server, add its init script to the default runlevels
  $ sudo systemctl start elasticsearch
    start elasticsearch
  $ check for runnig elasticsearch is runnin correct
    localhost:9200
  $ if status code is 503 write nano /ect/elasticsearch/elasticsearch.yml and type: discovery.zen.ping.multicast.enabled: false
    check localhost:9200 if status code is 200 it OK
5. Run this command for create database
  $ ./manage.py migrate
6. Now you can loaded database content from dump dir
  $ ./manage.py loaddata db.json
If all commands done successfully you can run the server with command
  $ ./manage.py runserver

Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run manage.py test
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ py.test

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html



Celery
^^^^^^

This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    cd ooba
    celery -A apps.taskapp worker -l info

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.





Sentry
^^^^^^

Sentry is an error logging aggregator service. You can sign up for a free account at  https://sentry.io/signup/?code=cookiecutter  or download and host it yourself.
The system is setup with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.


Deployment
----------

The following details how to deploy this application.


Webpack build
-------------


 ./node_modules/.bin/webpack --progress
