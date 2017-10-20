__author__ = 'akoikelov'

from allauth.utils import get_user_model
from allauth.account.models import EmailAddress

from apps.shop.models import *
from apps.category.models import *
from apps.global_category.models import *

def dict_has_keys(keys, dict):
    for k in keys:
        if k not in dict:
            return False

    return True


def assert_status_code(context, response, status_code):
    context.test.assertEqual(response['Content-Type'], 'application/json')
    context.test.assertEqual(response.status_code, status_code)


def assert_response_json_keys_exist(context, response, keys):
    json_content = response.json()

    context.test.assertTrue(dict_has_keys(keys, json_content))


def create_user(faker):
    username = faker.name()[0]
    email = '%s@somemail.com' % username
    password = '%s_password' % username

    user = get_user_model().objects.create(username=username, email=email)
    user.set_password(password)
    user.save()

    email_address = EmailAddress.objects.create(user=user, email=email, verified=True, primary=True)

    return dict(user=user, email_address=email_address, username=username, email=email, password=password)


def create_shop(faker, user=None, slug_prefix='', default_title=None):
    title = default_title if default_title is not None else faker.name()[0]
    slug = '%s_slug_%s' % (slug_prefix, title)
    short_description = 'some description'

    shop = Shop.objects.create(title=title, email=faker.email(), short_description=short_description, slug=slug)

    if user is not None:
        shop.user = [user]
        shop.save()

    return dict(title=title, slug=slug, short_description=short_description, shop=shop)


def create_category(faker, slug_prefix='', order=0, section=None, parent_category=None, is_global=False):
    title = faker.name()[0]
    slug = '%s_slug_%s' % (slug_prefix, title)

    if is_global:
        category = GlobalCategory.objects.create(title=title, slug=slug)
    else:
        category = Category.objects.create(title=title, slug=slug, section=section, parent=parent_category, order=order)

    return dict(title=title, slug=slug, category=category)


def do_request_to_login(context, url, email, password):
    return context.client.post(url, {
        'email': email, 'password': password
    })


def login_and_get_auth_token(context, url, email, password):
    response = do_request_to_login(context, url, email, password)

    assert_status_code(context, response, 200)
    json_content = response.json()

    if 'key' not in json_content:
        raise Exception('login action failed')

    return json_content['key']