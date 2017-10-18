from behave import *
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from features.helpers import *
from apps.shop.models import *
import os

use_step_matcher("re")

SHOPS_QUANTITY = 5
USER_INFO_URL = reverse('api:user_detail')


@given("user with list of shops")
def step_impl(context):
    faker = context.faker
    user_data = create_user(faker)
    user = user_data['user']
    auth_token = login_and_get_auth_token(context, '/api/v1/rest-auth/login/', user_data['email'], user_data['password'])

    img = SimpleUploadedFile(name='category.png', content=open('%s/../assets/category_icon.png' % os.path.dirname(os.path.abspath(__file__)), 'rb').read(),
                             content_type='image/png')

    for i in range(0, SHOPS_QUANTITY):
        title = faker.name()[0]
        slug = 'slug_%s_%s' % (title, i)
        short_description = 'some description'

        shop = Shop(title=title, email=faker.email(), short_description=short_description, logo=img, slug=slug)
        shop.save()

        shop.user = [user]
        shop.save()

    context.auth_token = auth_token


@when('app sends request with auth token')
def step_impl(context):
    context.response = context.client.get(USER_INFO_URL, {}, **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with user information")
def step_impl(context):
    assert_status_code_and_content_type(context, context.response, 200, 'application/json')
    assert_response_json_keys_exist(context, ['status', 'address', 'favorites_count', 'cart_count', 'email',
                                              'first_name', 'phone', 'shops', 'username', 'last_name'])


@when('app sends request without auth token/with wrong auth token')
def step_impl(context):
    context.response = context.client.get(USER_INFO_URL, {}, **dict(HTTP_AUTHORIZATIOn='Token wrongtoken'))


@then("it should get 401 error status code")
def step_impl(context):
    assert_status_code_and_content_type(context, context.response, 401, 'application/json')