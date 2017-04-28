from django.shortcuts import render
from django.views import generic
from .models import Shop
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