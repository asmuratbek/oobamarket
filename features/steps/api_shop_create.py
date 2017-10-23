from behave import *
from features.helpers import *
from django.urls import reverse


from features.steps import IMAGE_ASSET_PATH
from features.steps import LOGIN_URL

use_step_matcher("re")

SHOP_CREATE_URL = reverse('api:shop_create')


def do_request(context, title=None, email=None, image_path=None):
    post_data = dict(short_description='', place_id=0)
    image = None

    if title is not None and email is not None:
        image = open(image_path, 'rb')
        post_data = dict(title=title, email=email, short_description='', place_id=0, logo=image)

    response = context.client.post(SHOP_CREATE_URL, post_data,
                                   **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))

    if image is not None:
        image.close()

    return response


@given("a registered user")
def step_impl(context):
    faker = context.faker
    user_data = create_user(faker)

    context.auth_token = login_and_get_auth_token(context, LOGIN_URL, user_data['email'], user_data['password'])


@when('app sends request to "api_shop_create" url with all required data')
def step_impl(context):
    faker = context.faker
    context.response = do_request(context, faker.name(), faker.email(), image_path=IMAGE_ASSET_PATH)


@then("it should get 201 code response with an information of created shop")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 201)
    assert_response_json_keys_exist(context, response, ['title', 'user', 'email', 'description',
                                                        'short_description', 'logo', 'published'])


@when('app sends request to "api_shop_create" url missing required data')
def step_impl(context):
    context.response = do_request(context)


@then("it should get 400 error code")
def step_impl(context):
    assert_status_code(context, context.response, 400)
