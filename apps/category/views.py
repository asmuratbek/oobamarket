from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, render_to_response
from django.views import generic
from apps.category.models import Category
from apps.global_category.models import GlobalCategory
from apps.product.models import Product
from apps.properties.models import Properties, Values
from django.forms.models import model_to_dict


def category_detail(request, global_slug, slug):
    category = Category.objects.get(slug=slug)
    global_category = get_object_or_404(GlobalCategory, slug=global_slug)
    _property = Properties.objects.filter(category=category.id)
    properties = list()
    for prop in _property:
        item = model_to_dict(prop)
        item['values'] = Values.objects.filter(properties=prop.id)
        properties.append(item)

    # print(properties)

    template = "category/category_detail.html"

    context = {
        "object": category,
        "properties": properties,
        "global_slug": global_slug,
    }
    return render(request, template, context)


def get_property_list(request):
    category = get_object_or_404(Category, id=request.GET.get('category'))
    properties = category.properties_set.all()
    template = 'product/property_list.html'
    return render(request, template, {'properties': properties})


def get_product_by_filter(request):
    data = list()

    for item in request.GET:
        prop = {
            "property": item,
            "value": request.GET.get(item)
        }
        data.append(prop)

    values = []
    for item in data:
        prop = get_object_or_404(Properties, slug=item['property'])
        value = get_object_or_404(Values, properties=prop, id=item['value'])
        values.append(value)

    products = list()
    if len(values) > 0:
        for product in Product.objects.filter(values__in=values).distinct():
            is_filters_correct = True
            for value in values:
                if value not in product.values.all():
                    is_filters_correct = False

            if is_filters_correct:
                products.append(product)
    else:
        products = Product.objects.all()

    data = {
        'object_list': products,
        'col': 4,
    }

    return render(request, 'product/product_list.html', data)


def get_category_from_global_category(request):
    global_category = get_object_or_404(GlobalCategory, title=request.GET.get('global_category'))
    categories = Category.objects.filter(section=global_category, parent=None)
    category_list = {'{}'.format(category.id): '{}'.format(category.title) for category in categories}
    data = {
        'category_list': category_list,
        'count': len(category_list)
    }
    return JsonResponse(data)


def get_subcategory_from_category(request):
    category = get_object_or_404(Category, title=request.GET.get('category'), section__title=request.GET.get('section'))
    categories = category.get_descendants()
    category_list = {'{}'.format(category.id): '{}'.format(category.title) for category in categories}
    data = {
        'category_list': category_list,
        'count': len(category_list)
    }
    return JsonResponse(data)


@login_required
def get_category(request):
    if request.user.is_superuser and request.is_ajax:
        cat_id = request.GET.get('cat_id', '')
        try:
            category = Category.objects.get(id=cat_id)
        except Category.DoesNotExist:
            return JsonResponse({'parent_id': GlobalCategory.objects.first().id, 'cat_null': True})
        except ValueError:
            return JsonResponse({'parent_id': GlobalCategory.objects.first().id, 'cat_null': True})
        return JsonResponse({'parent_id': category.section.id})
    return HttpResponseBadRequest('User is not a superuser.')


def mail_confirm_view(request):
    return render(request, 'b85b738ce8c6.html', {})
