import json
from behave import *
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


@given("registered user")
def step_impl(context):
    faker = context.faker

    username = faker.name()[0]
    email = '%s@somemail.com' % username
    password = '%s_password' % username

    create_user(username, email, password)

    context.user = dict(username=username, plain_password=password, email=email)


@when('app sends right credentials to "/api/v1/rest-auth/login/"')
def step_impl(context):
    user = context.user
    do_request_to_login(context, '/api/v1/rest-auth/login/', user['email'], user['plain_password'])


@then("it should get authentication token")
def step_impl(context):
    assert_response(context, 200, 'key')


@when('app sends credentials with wrong username to "/api/v1/rest-auth/login/"')
def step_impl(context):
    user = context.user
    username_wrong = '%s_wrong' % user['username']

    do_request_to_login(context, '/api/v1/rest-auth/login/', username_wrong, user['plain_password'])


@then("it should get message saying that username is invalid")
def step_impl(context):
    assert_response(context, 400, 'email')


@when('app sends credentials with wrong password to "/api/v1/rest-auth/login/"')
def step_impl(context):
    user = context.user
    password_wrong = '%s_wrong' % user['plain_password']

    do_request_to_login(context, '/api/v1/rest-auth/login/', user['email'], password_wrong)


@then("it should get message saying that password is invalid")
def step_impl(context):
    assert_response(context, 400, 'non_field_errors')