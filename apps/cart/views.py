from django.shortcuts import render
from .models import Cart
from django.views import generic
# Create your views here.


class CartDetailView(generic.DetailView):
    model = Cart
