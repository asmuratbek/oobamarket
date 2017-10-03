from selenium import webdriver
from django.test import Client


def before_all(context):
    context.client = Client()
    # context.browser = webdriver.Firefox()
    # context.browser.implicitly_wait(5)
    # context.server_url = 'http://localhost:8000'


def after_all(context):
    pass
    # context.browser.quit()


def before_feature(context, feature):
    pass


def before_scenario(context, scenario):
    pass
