from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View

from apps.global_category.models import GlobalCategory
from .models import *
# Create your views here.


class UserFavoritesListView(LoginRequiredMixin, ListView):
    model = FavoriteProduct
    template_name = 'users/favorites.html'


# class ProductDetailView(DetailView):
#     model = Product


class FavoriteCreateView(LoginRequiredMixin, View):

    def get(self, request):
        item_id = request.GET.get("item")
        favorite, created = FavoriteProduct.objects.get_or_create(product_id=item_id, user=request.user)
        if not created:
            favorite.delete()
        favorites_count = request.user.get_favorites_count()
        data = {
            "created": created,
            "favorites_count": favorites_count,
        }
        return JsonResponse(data)

def product_detail(request, global_slug, category_slug, slug):
    product = get_object_or_404(Product, slug=slug)
    category = get_object_or_404(Category, slug=category_slug)
    global_category = get_object_or_404(GlobalCategory, slug=global_slug)
    template = "product/product_detail.html"
    context = {
        "object": product
    }
    return render(request, template, context)
