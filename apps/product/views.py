from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin

from apps.global_category.models import GlobalCategory
from .models import *
# Create your views here.


# class UserFavoritesListView(LoginRequiredMixin, ListView):
#     model = FavoriteProduct
#     template_name = 'users/favorites.html'


# class ProductDetailView(DetailView):
#     model = Product


def product_detail(request, global_slug, category_slug, slug):
    product = get_object_or_404(Product, slug=slug)
    category = get_object_or_404(Category, slug=category_slug)
    global_category = get_object_or_404(GlobalCategory, slug=global_slug)
    template = "product/product_detail.html"
    context = {
        "object": product
    }
    return render(request, template, context)

# def is_favorite(request, product_id):
#     if request.is_ajax():
#         product = Product.objects.get(product_id=id)
#         favorite = product.favorite



class FavoriteDetailView(SingleObjectMixin, View):
    model = FavoriteProduct
    template_name = "users/favorites.html"

    def get_object(self, *args, **kwargs):
        self.request.session.set_expiry(0)  # 5 minutes
        product_id = self.request.session.get("product_id")
        if product_id == None:
            favorite = FavoriteProduct()
            favorite.save()
            favorite_id = favorite.id
            self.request.session["cart_id"] = favorite_id
        favorite = FavoriteProduct.objects.get(id=favorite_id)
        if self.request.user.is_authenticated():
            favorite.user = self.request.user
            favorite.save()
        return favorite

    def get(self, request, *args, **kwargs):
        favorite = self.get_object()
        item_id = request.GET.get("item")
        delete_item = request.GET.get("delete", False)
        flash_message = ""
        item_added = False
        if item_id:
            item_instance = get_object_or_404(Product, id=item_id)
            qty = request.GET.get("qty", 1)
            try:
                if int(qty) < 1:
                    delete_item = True
            except:
                raise Http404
            favorite_item, created = FavoriteProduct.objects.get_or_create(favorite=favorite, product=item_instance, total=200)
            if created:
                flash_message = "Successfully added to the favorite"
                item_added = True
            if delete_item:
                flash_message = "Item removed successfully."
                favorite_item.delete()
            if not request.is_ajax():
                return HttpResponseRedirect('/')
                # return cart_item.cart.get_absolute_url()

        if request.is_ajax():
            try:
                is_favorite = favorite_item.product
            except:
                is_favorite = None

            data = {
                "deleted": delete_item,
                "is_favorite": is_favorite,
                "item_added": item_added,
                "flash_message": flash_message,
            }

            return JsonResponse(data)

        context = {
            "object": self.get_object()
        }
        template = self.template_name
        return render(request, template, context)

