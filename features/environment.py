from django.test import Client
from faker import Faker
from config.settings.base import MEDIA_ROOT
import os
import glob
import shutil
from django.core.management import call_command


def before_all(context):
    context.client = Client()
    context.faker = Faker()


def after_all(context):
    files = glob.glob('%s/*' % MEDIA_ROOT)

    for file in files:
        if os.path.isfile(file):
            os.remove(file)
        else:
            shutil.rmtree(file)


def before_feature(context, feature):
    call_command('flush', verbosity=0, interactive=False)


def before_scenario(context, scenario):
    pass
