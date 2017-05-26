from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from apps.category.models import Category
from apps.global_category.models import GlobalCategory


def category_detail(request, global_slug, slug):
    category = get_object_or_404(Category, slug=slug)
    global_category = get_object_or_404(GlobalCategory, slug=global_slug)
    template = "category/category_detail.html"
    context = {
        "object": category,
    }
    return render(request, template, context)

def get_category_from_global_category(request):
    global_category = get_object_or_404(GlobalCategory, title=request.GET.get('global_category'))
    categories = Category.objects.filter(section=global_category)
    category_list = {'{}'.format(category.id) : '{}'.format(category.title) for category in categories}
    data = {
        'category_list': category_list,
        'count': len(category_list)
    }
    return JsonResponse(data)


def get_subcategory_from_category(request):
    category = get_object_or_404(Category, title=request.GET.get('category'))
    categories = Category.objects.filter(parent=category)
    category_list = {'{}'.format(category.id) : '{}'.format(category.title) for category in categories}
    data = {
        'category_list': category_list,
        'count': len(category_list)
    }
    return JsonResponse(data)
