from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic.detail import SingleObjectMixin

from apps.product.models import Product
from .models import Cart, CartItem
from django.views import View


# Create your views here.

def get_summ(items):
    total = 0
    for i in items:
        total += i.total
    return total


class CartDetailView(SingleObjectMixin, View):
    model = Cart
    template_name = "cart/cart_detail.html"

    def get_object(self, *args, **kwargs):
        self.request.session.set_expiry(0)  # 5 minutes
        cart_id = self.request.session.get("cart_id", "")
        if cart_id == "":
            cart = Cart()
            cart.save()
            cart_id = cart.id
            self.request.session["cart_id"] = cart_id
        cart = Cart.objects.get(id=cart_id)
        if self.request.user.is_authenticated():
            cart.user = self.request.user
            cart.save()
        return cart

    def get(self, request, *args, **kwargs):
        cart = self.get_object()
        # shops = cart.get_shops()
        # total_by_shop = dict()
        # for shop in shops:
        #     items = cart.cartitem_set.filter(product__shop=shop)
        #     total_by_shop[shop.title] = get_summ(items)
        item_id = request.GET.get("item", "")
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

            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=item_instance)
            if created:
                flash_message = "Продукт успешно добавлен в корзину"
                item_added = True
            # elif not created and cart_item.quantity == qty:
            #     delete_item = True
            if delete_item:
                flash_message = "Продукт успешно удален из корзины"
                cart_item.delete()
            else:
                if not created:
                    flash_message = "Количество продукта изменено"
                cart_item.quantity = qty
                text = request.GET.get('text', "")
                if text:
                    cart_item.comments = text
                cart_item.save()
            if not request.is_ajax():
                return HttpResponseRedirect(reverse("cart:detail"))
                # return cart_item.cart.get_absolute_url()

        if request.is_ajax():
            try:
                total = cart_item.total
            except:
                total = None
            try:
                id = cart_item.product.id
            except:
                id = None
            try:
                subtotal = cart_item.cart.subtotal
            except:
                subtotal = None

            try:
                cart_total = cart_item.cart.total
            except:
                cart_total = None

            try:
                total_items = cart_item.cart.cartitem_set.count()
            except:
                total_items = 0

            data = {
                "deleted": delete_item,
                "item_added": item_added,
                "line_total": total,
                "subtotal": subtotal,
                "cart_total": cart_total,
                "flash_message": flash_message,
                "total_items": total_items,
                "id": id
            }

            return JsonResponse(data)

        context = {
            "object": self.get_object()
        }
        template = self.template_name
        return render(request, template, context)
