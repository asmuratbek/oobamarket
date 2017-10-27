from behave import *
from features.steps import *
from features.helpers import *
from django.urls import reverse

use_step_matcher("re")


@given("some product we want to delete")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='product_delete_')
    product_info = instances['product_info']
    user_info = instances['user_info']
    product = product_info['product']

    context.product_id = product.id
    context.product_slug = product_info['slug']
    context.auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])


@when('app sends request to "api_product_delete" url with the product slug')
def step_impl(context):
    context.response = context.client.post(reverse('api:product_delete', kwargs=dict(slug=context.product_slug)),
                                           data={}, **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@then("it should get response with product delete success status")
def step_impl(context):
    assert_status_code(context, context.response, 200)
    context.test.assertIsNone(Product.objects.filter(id=context.product_id).first())
