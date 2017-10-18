__author__ = 'akoikelov'

from allauth.utils import get_user_model
from allauth.account.models import EmailAddress


def dict_has_keys(keys, dict):
    for k in keys:
        if k not in dict:
            return False

    return True


def assert_status_code_and_content_type(context, response, status_code, content_type):
    context.test.assertEqual(response['Content-Type'], content_type)
    context.test.assertEqual(response.status_code, status_code)


def assert_response_json_keys_exist(context, keys):
    response = context.response
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


def do_request_to_login(context, url, email, password):
    return context.client.post(url, {
        'email': email, 'password': password
    })


def login_and_get_auth_token(context, url, email, password):
    response = do_request_to_login(context, url, email, password)

    context.test.assertEqual(response.status_code, 200)
    json_content = response.json()

    if 'key' not in json_content:
        raise Exception('login action failed')

    return json_content['key']