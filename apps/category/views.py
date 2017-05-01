from django.shortcuts import get_object_or_404, render
from django.views import generic
from apps.category.models import Category
from apps.global_category.models import GlobalCategory


def category_detail(request, global_slug, slug):
    category = get_object_or_404(Category, slug=slug)
    global_category = get_object_or_404(GlobalCategory, slug=global_slug)
    template = "category/category_detail.html"
    context = {
        "object": category
    }
    return render(request, template, context)

