__author__ = 'akoikelov'

from allauth.utils import get_user_model
from allauth.account.models import EmailAddress


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