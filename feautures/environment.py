from selenium import webdriver


def before_all(context):
    context.browser = webdriver.Firefox()
    context.browser.implicitly_wait(5)
    context.server_url = 'http://localhost:8000'


def after_all(context):
    context.browser.quit()


def before_feature(context, feature):
    pass
