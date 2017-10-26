from behave import *
from features.steps import *
from features.helpers import *
from django.urls import reverse

use_step_matcher("re")


@given("some user we want to update")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='user_update_')
    user_info = instances['user_info']
    new_data = dict(first_name=faker.name(), last_name='%s_last' % faker.name(),
                    address=faker.address(), email=faker.email(), username='username_%s' % faker.email())

    context.auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])
    context.user_id = user_info['user'].id
    context.new_data = new_data


@when('app sends request to "api_user_update" url with valid data')
def step_impl(context):
    post_data = context.new_data
    context.response = context.client.post(reverse('api:user_detail'), data=post_data,
                                           **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with user update success status")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['status', 'message'])
    json_content = response.json()

    context.test.assertEqual(json_content['status'], 0)

    new_data = context.new_data
    user = User.objects.get(id=context.user_id)

    context.test.assertEqual(user.first_name, new_data['first_name'])
    context.test.assertEqual(user.last_name, new_data['last_name'])
    context.test.assertEqual(user.address, new_data['address'])
    context.test.assertEqual(user.email, new_data['email'])
    context.test.assertEqual(user.username, new_data['username'])


@when('app sends request to "api_user_update" url with invalid data')
def step_impl(context):
    post_data = context.new_data

    del post_data['email']
    del post_data['username']

    context.response = context.client.post(reverse('api:user_detail'), data=post_data,
                                           **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with user update fail status")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['status', 'message'])
    json_content = response.json()

    context.test.assertEqual(json_content['status'], 1)