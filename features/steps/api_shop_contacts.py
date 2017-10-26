from behave import *
from django.urls import reverse
from features.helpers import *

use_step_matcher("re")

SHOP_CONTACTS_QUANTITY = 3


@given("shop with its contacts")
def step_impl(context):
    faker = context.faker
    shop_data = create_shop(faker, slug_prefix='contacts')
    shop = shop_data['shop']

    for i in range(0, SHOP_CONTACTS_QUANTITY):
        Contacts.objects.create(address=faker.address(), phone=faker.text(), shop=shop)

    context.shop_slug = shop_data['slug']


@when('app sends request to "api_shop_contacts" url containing a slug of the shop')
def step_impl(context):
    context.response = context.client.get(reverse('api:shop_contacts', kwargs=dict(slug=context.shop_slug)))


@then("it should get response with list of contacts info")
def step_impl(context):
    response = context.response

    assert_status_code(context, response, 200)
    assert_response_json_keys_exist(context, response, ['status', 'contacts'])


@when('app sends request to "api_shop_contacts" url containing non-existing slug')
def step_impl(context):
    context.response = context.client.get(reverse('api:shop_contacts', kwargs=dict(slug='non_existing_slug')))
