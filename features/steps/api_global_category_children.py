from behave import *
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.global_category.models import GlobalCategory
from apps.category.models import Category

import json
from features.helpers import *
import os

use_step_matcher("re")

GLOBAL_CATEGORY_CHILDREN_CATEGORIES_QUANTITY = 5


@given("prepared global category with children categories")
def step_impl(context):
    gc_title = context.faker.name()
    gc_slug = 'slug_%s' % context.faker.words()[0]
    global_category = GlobalCategory.objects.create(title=gc_title, slug=gc_slug)

    global_category.save()

    img = SimpleUploadedFile(name='category.png', content=open('%s/../assets/global_category_icon.png' % os.path.dirname(os.path.abspath(__file__)), 'rb').read(),
                             content_type='image/png')

    for i in range(0, GLOBAL_CATEGORY_CHILDREN_CATEGORIES_QUANTITY):
        cc_title = context.faker.name()
        child_category = Category.objects.create(title=cc_title, slug='child_slug_%s' % context.faker.words()[0], image=img,
                                                 section=global_category, order=i)
        child_category.save()

    context.global_category_slug = gc_slug


@when('app sends request to "/api/v1/globalcategory/<slug>/children/"')
def step_impl(context):
    context.response = context.client.get('/api/v1/globalcategory/%s/children/' % context.global_category_slug)


@then("it should get response with list of children categories")
def step_impl(context):
    response = context.response

    assert_status_code_and_content_type(context, response, 200, 'application/json')

    items = json.loads(str(response.content, encoding='utf8'))
    context.test.assertEqual(len(items), GLOBAL_CATEGORY_CHILDREN_CATEGORIES_QUANTITY)

    for item in items:
        context.test.assertTrue(dict_has_keys(['id', 'title', 'slug', 'parent_id'], item))