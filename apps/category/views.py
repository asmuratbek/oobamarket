from django.shortcuts import render
from django.views import generic

# Create your views here.
from apps.category.models import GlobalCategory
from apps.product.models import Product
from apps.shop.models import Shop


class IndexView(generic.ListView):
    model = GlobalCategory
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['shops'] = Shop.objects.all()
        context["weeks_best_products"] = Product.week_best.all()
        return context


class GlobalDetailView(generic.DetailView):
    model = GlobalCategory
