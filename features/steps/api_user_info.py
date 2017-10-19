from behave import *
from django.urls import reverse
from features.helpers import *
from apps.shop.models import *

use_step_matcher("re")

SHOPS_QUANTITY = 5
USER_INFO_URL = reverse('api:user_detail')
LOGIN_URL = reverse('api:rest_login')


@given("user with list of shops")
def step_impl(context):
    faker = context.faker
    user_data = create_user(faker)
    user = user_data['user']
    auth_token = login_and_get_auth_token(context, LOGIN_URL, user_data['email'], user_data['password'])

    for i in range(0, SHOPS_QUANTITY):
        title = faker.name()[0]
        slug = 'slug_%s_%s' % (title, i)
        short_description = 'some description'

        shop = Shop.objects.create(title=title, email=faker.email(), short_description=short_description, slug=slug)
        shop.user = [user]
        shop.save()

    context.auth_token = auth_token


@when('app sends request with auth token')
def step_impl(context):
    context.response = context.client.get(USER_INFO_URL, {}, **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with user information")
def step_impl(context):
    assert_status_code(context, context.response, 200)
    assert_response_json_keys_exist(context, ['status', 'address', 'favorites_count', 'cart_count', 'email',
                                              'first_name', 'phone', 'shops', 'username', 'last_name'])


@when('app sends request without auth token/with wrong auth token')
def step_impl(context):
    context.response = context.client.get(USER_INFO_URL, {}, **dict(HTTP_AUTHORIZATIOn='Token wrongtoken'))


@then("it should get 401 error status code")
def step_impl(context):
    assert_status_code(context, context.response, 401)