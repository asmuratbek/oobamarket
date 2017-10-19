from behave import then
from features.helpers import assert_status_code

__author__ = 'akoikelov'


@then("it should get 404 error code")
def step_impl(context):
    assert_status_code(context, context.response, 404)