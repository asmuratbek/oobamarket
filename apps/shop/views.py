from django.shortcuts import render
from django.views import generic
from .models import Shop
# Create your views here.


class ShopDetailView(generic.DetailView):
    model = Shop
