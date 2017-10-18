from behave import *
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from apps.global_category.models import GlobalCategory
from apps.category.models import Category

from features.helpers import *
import os


use_step_matcher("re")

SUBCATEGORY_CHILDREN_CATEGORIES_QUANTITY = 5


@given("prepared subcategory with children categories")
def step_impl(context):
    gc_title = context.faker.name()
    gc_slug = 'slug_%s' % context.faker.words()[0]
    global_category = GlobalCategory.objects.create(title=gc_title, slug=gc_slug)

    global_category.save()

    img = SimpleUploadedFile(name='category.png', content=open('%s/../assets/category_icon.png' % os.path.dirname(os.path.abspath(__file__)), 'rb').read(),
                             content_type='image/png')

    subcategory_title = context.faker.name()
    subcategory_slug = 'subcategory_slug_%s' % context.faker.words()[0]
    subcategory = Category.objects.create(title=subcategory_title, slug=subcategory_slug, section=global_category,
                                          image=img)

    subcategory.save()

    for i in range(0, SUBCATEGORY_CHILDREN_CATEGORIES_QUANTITY):
        cc_title = context.faker.name()
        child_category = Category.objects.create(title=cc_title, slug='child_slug_%s_%s' % (context.faker.words()[0], i), image=img,
                                                 section=global_category, order=i, parent=subcategory)
        child_category.save()

    context.subcategory_slug = subcategory_slug


@when('app sends request to "api_category_children" url')
def step_impl(context):
    context.response = context.client.get(reverse('api:category_children', kwargs={'slug': context.subcategory_slug}))


@then("it should get response with list of given subcategory's children categories")
def step_impl(context):
    response = context.response

    assert_status_code_and_content_type(context, response, 200, 'application/json')

    items = response.json()
    context.test.assertEqual(len(items), SUBCATEGORY_CHILDREN_CATEGORIES_QUANTITY)

    for item in items:
        context.test.assertTrue(dict_has_keys(['id', 'title', 'slug', 'parent_id'], item))
        context.test.assertIsNotNone(item['parent_id'])