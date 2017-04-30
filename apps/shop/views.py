from django.shortcuts import render
from django.views import generic

from apps.product.models import Product
from .models import Shop, Banners
# Create your views here.


class ShopDetailView(generic.DetailView):
    model = Shop


def create(request):

    params = {
        'shop': 'shop'
    }

    return render(request, 'shop/create.html', params)

def agreement(request):

    params = {
        'shop': 'shop'
    }

    return render(request, 'shop/agreement.html', params)
