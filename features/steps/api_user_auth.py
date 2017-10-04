import json
from allauth.account.models import EmailAddress
from behave import *
from allauth.utils import get_user_model
from features.helpers import *

use_step_matcher("re")

# helper functions


def do_request_to_login(context, url, email, password):
    context.response = context.client.post(url, {
        'email': email, 'password': password
    })


def assert_response(context, status_code, expected_key_in_json):
    response = context.response

    assert_status_code_and_content_type(context, response, status_code, 'application/json')

    json_content = json.loads(str(response.content, encoding='utf8'))
    context.test.assertTrue(expected_key_in_json in json_content)


@given("registered user with username (?P<username>.+), email (?P<email>.+) and password (?P<password>.+)")
def step_impl(context, username, email, password):
    user = get_user_model().objects.create(username=username, email=email)
    user.set_password(password)
    user.save()

    context.email_address = EmailAddress.objects.create(user=user, email=email, verified=True, primary=True)
    context.user = dict(username=username, plain_password=password, email=email)


@when('app sends credentials to "/api/v1/rest-auth/login/"')
def step_impl(context):
    user = context.user
    do_request_to_login(context, '/api/v1/rest-auth/login/', user['email'], user['plain_password'])


@then("it should get authentication token")
def step_impl(context):
    assert_response(context, 200, 'key')


@when('app sends credentials with wrong username (?P<username_wrong>.+) to "/api/v1/rest-auth/login/"')
def step_impl(context, username_wrong):
    user = context.user
    do_request_to_login(context, '/api/v1/rest-auth/login/', username_wrong, user['plain_password'])


@then("it should get message saying that username is invalid")
def step_impl(context):
    assert_response(context, 400, 'email')


@when('app sends credentials with wrong password (?P<password_wrong>.+) to "/api/v1/rest-auth/login/"')
def step_impl(context, password_wrong):
    user = context.user
    do_request_to_login(context, '/api/v1/rest-auth/login/', user['email'], password_wrong)


@then("it should get message saying that password is invalid")
def step_impl(context):
    assert_response(context, 400, 'non_field_errors')