from behave import *

use_step_matcher("re")


@given("registered user with username (?P<username>.+), email (?P<email>.+) and password (?P<password>.+)")
def step_impl(context, username, email, password):
    pass


@when('app sends credentials to "/rest-auth/login"')
def step_impl(context):
    pass


@then("it should get authentication token")
def step_impl(context):
    pass


@when('app sends credentials with wrong username (?P<username_wrong>.+) to "/rest-auth/login"')
def step_impl(context, username_wrong):
    pass


@then("it should get message saying that username is invalid")
def step_impl(context):
    pass


@when('app sends credentials with wrong password (?P<password_wrong>.+) to "/rest-auth/login"')
def step_impl(context, password_wrong):
    pass


@then("it should get message saying that password is invalid")
def step_impl(context):
    pass