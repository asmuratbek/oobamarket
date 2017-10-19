from behave import *
from features.helpers import *
from django.urls import reverse

use_step_matcher("re")

# helper functions

LOGIN_URL = reverse('api:rest_login')


@given("registered user")
def step_impl(context):
    data = create_user(context.faker)

    username = data['username']
    email = data['email']
    password = data['password']

    context.user = dict(username=username, plain_password=password, email=email)


@when('app sends right credentials')
def step_impl(context):
    user = context.user
    context.response = do_request_to_login(context, LOGIN_URL, user['email'], user['plain_password'])


@then("it should get authentication token")
def step_impl(context):
    assert_status_code(context, context.response, 200)
    assert_response_json_keys_exist(context, ['key'])


@when('app sends credentials with wrong username')
def step_impl(context):
    user = context.user
    username_wrong = '%s_wrong' % user['username']

    context.response = do_request_to_login(context, LOGIN_URL, username_wrong, user['plain_password'])


@then("it should get message saying that username is invalid")
def step_impl(context):
    assert_status_code(context, context.response, 400)
    assert_response_json_keys_exist(context, ['email'])


@when('app sends credentials with wrong password')
def step_impl(context):
    user = context.user
    password_wrong = '%s_wrong' % user['plain_password']

    context.response = do_request_to_login(context, LOGIN_URL, user['email'], password_wrong)


@then("it should get message saying that password is invalid")
def step_impl(context):
    assert_status_code(context, context.response, 400)
    assert_response_json_keys_exist(context, ['non_field_errors'])