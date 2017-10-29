from behave import *
from features.steps import *
from features.helpers import *
from django.urls import reverse
from django.test.client import MULTIPART_CONTENT

use_step_matcher("re")


@given("some product which should be updated")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='product_update_')
    user_info = instances['user_info']
    product_info = instances['product_info']
    shop_info = instances['shop_info']
    global_category_info = instances['global_category_info']
    new_category_info = create_category(faker, slug_prefix='product_update_new_category_', order=1,
                                        section=global_category_info['category'])

    new_data = dict(title=faker.words()[0], price=random.randint(10, 10000))

    context.new_data = new_data
    context.new_category_slug = new_category_info['slug']
    context.shop_slug = shop_info['slug']
    context.product_slug = product_info['slug']
    context.auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])


@when('app sends request to "api_product_update" url with all required data')
def step_impl(context):
    image = open(IMAGE_ASSET_PATH, 'rb')
    new_data = context.new_data
    post_data = dict(shop=context.shop_slug, category=context.new_category_slug,
                     title=new_data['title'], price=new_data['price'], images_files=[image])

    context.response = context.client.post(reverse('api:product_update', kwargs=dict(slug=context.product_slug)),
                                           data=post_data, content_type=MULTIPART_CONTENT,
                                           **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))
    image.close()


@then("it should get response with update success status")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    product = Product.objects.get(slug=context.product_slug)
    new_data = context.new_data

    context.test.assertEqual(product.title, new_data['title'])
    context.test.assertEqual(product.price, new_data['price'])
    context.test.assertEqual(product.category, Category.objects.get(slug=context.new_category_slug))


@when('app sends request to "api_product_update" url with invalid shop slug')
def step_impl(context):
    new_data = context.new_data
    post_data = dict(shop='invalid_shop_slug', category=context.new_category_slug,
                     title=new_data['title'], price=new_data['price'])

    context.response = context.client.post(reverse('api:product_update', kwargs=dict(slug=context.product_slug)),
                                           data=post_data, content_type=MULTIPART_CONTENT,
                                           **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))


@when('app sends request to "api_product_update" url with invalid category slug')
def step_impl(context):
    new_data = context.new_data
    post_data = dict(shop=context.shop_slug, category='invalid_category_slug',
                     title=new_data['title'], price=new_data['price'])

    context.response = context.client.post(reverse('api:product_update', kwargs=dict(slug=context.product_slug)),
                                           data=post_data, content_type=MULTIPART_CONTENT,
                                           **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))
