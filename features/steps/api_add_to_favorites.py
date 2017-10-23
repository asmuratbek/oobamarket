from behave import *
from features.steps import LOGIN_URL
from features.helpers import *
from apps.product.models import *

use_step_matcher("re")


@given("a product which user wants to add to favorites list")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='prefix_one_favorite')
    user_info = instances['user_info']
    product_info = instances['product_info']

    auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])

    context.auth_token = auth_token
    context.product_slug = product_info['slug']
    context.user = user_info['user']
    context.product = product_info['product']


@when('app sends request to "api_add_to_favorites" url with given product slug')
def step_impl(context):
    context.response = context.client.post(reverse('api:product_add_to_favorite', kwargs=dict(slug=context.product_slug)),
                                           **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with info that product is added to favorites")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    json_content = response.json()

    assert_response_json_keys_exist(context, response, ['status', 'message'])

    context.test.assertEqual(json_content['status'], 'success')
    context.test.assertEqual(json_content['message'], 'added to favorites list')

    favorite_product = FavoriteProduct.objects.filter(user=context.user, product=context.product)
    context.test.assertIsNotNone(favorite_product)


@given("a product which already added to favorites list")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='prefix_one')
    user_info = instances['user_info']
    product_info = instances['product_info']

    FavoriteProduct.objects.create(user=user_info['user'], product=product_info['product'])

    auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])

    context.auth_token = auth_token
    context.product_slug = product_info['slug']
    context.product = product_info['product']
    context.user = user_info['user']

    context.test.assertIsNotNone(FavoriteProduct.objects.filter(user=user_info['user'], product=product_info['product']).first())


@then("it should get response with info that product is removed from favorites")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    json_content = response.json()

    assert_response_json_keys_exist(context, response, ['status', 'message'])

    context.test.assertEqual(json_content['status'], 'success')
    context.test.assertEqual(json_content['message'], 'deleted from favorite')

    context.test.assertIsNone(FavoriteProduct.objects.filter(user=context.user, product=context.product).first())