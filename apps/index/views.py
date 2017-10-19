from django.shortcuts import render

# Create your views here.
from django.views import generic

from apps.product.models import Product
from apps.shop.models import Shop
from .models import IndexBlocks, PremiumIndexBlocks, BLOCK_TYPES
from itertools import zip_longest


class IndexView(generic.TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['shops'] = Shop.objects.all()[:12]
        if self.request.user.is_authenticated:
            context['subscribe_shops'] = [sub.subscription.id for sub in self.request.user.subscription_set.all()]
        context["weeks_best_products"] = Product.objects.all()[:12]
        first_col = IndexBlocks.objects.filter(column='first_col').order_by('row')
        second_col = IndexBlocks.objects.filter(column='second_col').order_by('row')
        third_col = IndexBlocks.objects.filter(column='third_col').order_by('row')
        blocks = list(zip_longest(first_col, second_col, third_col))
        context['blocks'] = [i for c in blocks for i in c]
        premium_blocks = {k: v for k, d in BLOCK_TYPES for v in PremiumIndexBlocks.objects.all() if v.block_type == k}
        context.update(premium_blocks)
        return context
