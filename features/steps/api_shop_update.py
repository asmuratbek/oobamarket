from behave import *
from django.test.client import MULTIPART_CONTENT
from features.steps import *
from features.helpers import *
from django.urls import reverse

use_step_matcher("re")


@given("some shop which info we want to update")
def step_impl(context):
    faker = context.faker
    instances = create_instances(faker, slug_prefix='shop_update_')
    user_info = instances['user_info']
    shop_info = instances['shop_info']

    random_word = faker.words()[0]
    new_data = dict(title=random_word, short_description=random_word,
                    description=random_word, email=faker.email(), phone=random_word,
                    address=random_word, round_the_clock=True, monday=random_word,
                    tuesday=random_word, wednesday=random_word, thursday=random_word,
                    friday=random_word, saturday=random_word, sunday=random_word)

    context.new_data = new_data
    context.shop_slug = shop_info['slug']
    context.auth_token = login_and_get_auth_token(context, LOGIN_URL, user_info['email'], user_info['password'])


@when('app sends request to "api_shop_update" url with all required data')
def step_impl(context):
    image = open(IMAGE_ASSET_PATH, 'rb')
    post_data = context.new_data
    post_data['new_logo'] = image

    context.response = context.client.post(reverse('api:shop_update', kwargs=dict(slug=context.shop_slug)),
                                           post_data, content_type=MULTIPART_CONTENT,
                                           **dict(HTTP_AUTHORIZATION='Token %s' % context.auth_token))

    image.close()


@then("it should get response with shop update success status")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)

    new_data = context.new_data
    shop = Shop.objects.get(slug=context.shop_slug)

    context.test.assertEqual(shop.title, new_data['title'])
    context.test.assertEqual(shop.short_description, new_data['short_description'])
    context.test.assertEqual(shop.description, new_data['description'])
    context.test.assertEqual(shop.email, new_data['email'])

    context.test.assertEqual(Contacts.objects.filter(shop=shop).count(), 1)