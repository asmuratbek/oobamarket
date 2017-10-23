from behave import then
from features.helpers import assert_status_code
import environ
from django.urls import reverse

__author__ = 'akoikelov'

IMAGE_ASSET_PATH = '%s/assets/category_icon.png' % (environ.Path(__file__) - 2)
LOGIN_URL = reverse('api:rest_login')


@then("it should get 404 error code")
def step_impl(context):
    assert_status_code(context, context.response, 404)