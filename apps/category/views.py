from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from apps.category.models import Category
from apps.global_category.models import GlobalCategory
from apps.product.models import Product
from apps.properties.models import Properties, Values


def category_detail(request, global_slug, slug):
    category = get_object_or_404(Category, slug=slug)
    global_category = get_object_or_404(GlobalCategory, slug=global_slug)
    property = Properties.objects.filter(category=category.id)
    value = []
    for prop in property:
        prop.value = Values.objects.filter(properties=prop.id)
        value = prop.value

    template = "category/category_detail.html"

    context = {
        "object": category,
        "property": property,
        "value": value,
    }
    return render(request, template, context)


def get_product_by_filter(request):
    value = get_object_or_404(Values, value=request.GET.get('value'))
    products = Product.objects.filter(values__products__values__in=[value])
    product_list = {'{}'.format(product.id): '{}'.format(product.title) for product in products}

    data = {
        'product': product_list,
    }

    return JsonResponse(data)


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
    category = get_object_or_404(Category, title=request.GET.get('category'))
    categories = Category.objects.filter(parent=category)
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
        except ValueError:
            return JsonResponse({'parent_id': GlobalCategory.objects.first().id, 'cat_null': True})
        return JsonResponse({'parent_id': category.section.id})
    return HttpResponseBadRequest
