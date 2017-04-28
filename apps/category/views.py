import random

import datetime

from django.core.files import File
from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic
from config.settings import base
# Create your views here.
from apps.category.models import GlobalCategory
from apps.category.models import Category
from apps.product.models import Product, ProductImage
from apps.shop.models import Shop
from apps.users.models import User


class IndexView(generic.ListView):
    model = GlobalCategory
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['shops'] = Shop.objects.all()
        context["weeks_best_products"] = Product.objects.all()[:8]
        return context


class GlobalDetailView(generic.DetailView):
    model = GlobalCategory



def fixtures(request, name):
    if name == 'product':
        for i in range(0, 21):
            post = Product()
            post.shop = Shop.objects.first()
            post.category = Category.objects.first()
            post.title = 'Продукт ' + str(random.randrange(1000, 9999))
            post.slug = 'slug' + str(random.randrange(1000, 9999))
            post.sell_count = 0
            post.discount = 0
            post.currency = 'сом'
            post.quantity = 21
            post.delivery_type = 'paid'
            post.delivery_cost = 0
            post.delivery_currency = 'сом'
            post.in_stock = True
            post.published = True
            post.save()
    elif name == 'product_delete':
        if Product.objects.all():
            for p in Product.objects.all():
                p.delete()

    elif name == 'shop':
        for i in range(0, 21):
            post = Shop()
            post.title = 'Shop '+ str(random.randrange(1000, 9999))
            post.slug = 'slug'+ str(random.randrange(1000, 9999))
            post.email = 'admin@gmail.com'
            post.short_decription = 'lorem ipsum dolor sit amet'
            post.description = 'lorem description'
            post.created_at = datetime.date.today()
            post.updated_ad = datetime.date.today()
            post.logo = base.STATIC_ROOT + 'news_image.png'
            post.save()
            post.user.add(User.objects.first())
    elif name == 'category':
        for i in range(0, 21):
            post = Category()
            post.parent = ''
            post.title = 'Категория' + str(random.randrange(1000, 9999))
            post.slug = 'slug' + str(random.randrange(1000, 9999))
            post.section = GlobalCategory.objects.first()
            post.created_at = datetime.date.today()
            post.updated_at = datetime.date.today()
            post.save()
    elif name == 'globalc':
        for i in range(0, 7):
            post = GlobalCategory()
            post.title = 'Гл. Категория ' + str(random.randrange(1000, 9999))
            post.slug = 'slug' + str(random.randrange(1000, 9999))
            post.created_at = datetime.date.today()
            post.updated_at = datetime.date.today()
            post.icon = 'images/sliders/news_image.png'
            post.save()

    return JsonResponse(dict(success=True, message='Heeey!'))

