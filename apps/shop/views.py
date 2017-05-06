from django.shortcuts import render
from django.views import generic
from django.views.generic import CreateView

from apps.product.models import Product
from .models import Shop, Banners
# Create your views here.


class ShopDetailView(generic.DetailView):
    model = Shop



class ShopCreateView(CreateView):
    model = Shop
    fields = ['title', 'logo', 'email', 'phone', 'short_description', 'description',]


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
