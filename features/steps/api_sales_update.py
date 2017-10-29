from behave import *
from django.test.client import MULTIPART_CONTENT
from features.steps import *
from features.helpers import *
from django.urls import reverse

use_step_matcher("re")


@given("some shop's sale")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='product_update_')
    user_info = instances['user_info']
    shop_info = instances['shop_info']
    sale_info = create_sales(faker, shop=shop_info['shop'])

    new_data = dict(title=faker.words()[0], short_description=faker.words()[0],
                    published=True, description=faker.words()[0], discount=random.randint(1, 80))

    context.new_data = new_data
    context.shop_slug = shop_info['slug']
    context.sale_id = sale_info['sale'].id
    context.auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])


@when('app sends request to "api_sales_update" url will all required data')
def step_impl(context):
    image = open(IMAGE_ASSET_PATH, 'rb')
    post_data = context.new_data
    post_data['image'] = image

    context.response = context.client.post(reverse('api:shop_sales_update', kwargs=dict(slug=context.shop_slug,
                                                                                 pk=context.sale_id)),
                                           post_data, content_type=MULTIPART_CONTENT,
                                           **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))

    image.close()


@then("it should get response with shop sale update success status")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)

    new_data = context.new_data
    sale = Sales.objects.get(id=context.sale_id)

    context.test.assertEqual(sale.title, new_data['title'])
    context.test.assertEqual(sale.short_description, new_data['short_description'])
    context.test.assertEqual(sale.published, new_data['published'])
    context.test.assertEqual(sale.description, new_data['description'])
    context.test.assertEqual(sale.discount, new_data['discount'])
