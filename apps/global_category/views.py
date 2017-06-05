import datetime
import random

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import generic

from apps.category.models import Category
from apps.global_category.models import GlobalCategory
from apps.product.models import Product
from apps.shop.models import Shop
from apps.users.models import User
from config.settings import base


class IndexView(generic.TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['shops'] = Shop.objects.all()
        context["weeks_best_products"] = Product.objects.all().order_by('-sell_count')[:8]
        return context


class GlobalDetailView(generic.DetailView):
    model = GlobalCategory
