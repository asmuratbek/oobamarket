import os
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import DetailView
from apps.product.models import Product
from apps.shop.models import Shop
from .models import Cart, CartItem
from django.views import View
from .mixins import CartOwnerUsers, ConfirmOrderByShopOwner


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
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=item_instance)
            try:
                if int(qty) < 1 or not created and cart_item.quantity == qty:
                    delete_item = True
            except:
                raise Http404


            if created:
                flash_message = "Продукт успешно добавлен в корзину"
                item_added = True
            # elif not created and cart_item.quantity == qty:
            #     delete_item = True
            if not created and qty == 1:
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


class CartDetailByPkUser(CartOwnerUsers, View):
    def get(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, id=kwargs.get('pk', ''))
        if cart.user == request.user or request.user.is_staff:
            template = 'cart/cart_detail_user.html'
            context = dict(object=cart)
            return render(request, template, context)
        else:
            raise Http404

    def post(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, id=kwargs.get('pk', ''))
        all_cartitems = cart.cartitem_set.values_list('id', flat=True)
        cartitems_ids = [int(i) for i in request.POST.getlist('item')]
        cartitem_text = request.POST.getlist('text')
        cartitem_qty = [int(q) for q in request.POST.getlist('qty')]
        combine_values = list(zip(cartitems_ids, cartitem_text, cartitem_qty))
        deleted_ids = list(set(all_cartitems).difference(set(cartitems_ids)))
        if deleted_ids:
            cart.cartitem_set.filter(id__in=deleted_ids).delete()
        for i, t, q in combine_values:
            cartitem = get_object_or_404(CartItem, id=i)
            if q < 1:
                cartitem.delete()
            else:
                cartitem.comments = t.strip()
                cartitem.quantity = q
                cartitem.save()
        return HttpResponseRedirect(reverse('cart:detail_by_pk_user', kwargs={'pk': cart.id,
                                                                              'username': request.user.username}))


class CartDetailByPkShop(CartOwnerUsers, View):
    def get(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, id=kwargs.get('pk', ''))
        shop = get_object_or_404(Shop, slug=kwargs.get('shop_slug', ''))
        items = cart.cartitem_set.filter(product__shop__user__id=request.user.id)
        if shop in cart.simpleorder.confirm_shops.all():
            status = 'confirmed'
        elif shop in cart.simpleorder.rejected_shops.all():
            status = 'rejected'
        else:
            status = 'none'
        template = 'cart/cart_detail_shops.html'
        context = dict(items=items, total_price=sum(items.values_list('total', flat=True)),
                       shop=shop, status=status)
        return render(request, template, context)


class ConfirmOrderByShop(ConfirmOrderByShopOwner, View):
    def post(self, request, *args, **kwargs):
        flag = request.POST.get('flag')
        cart = get_object_or_404(Cart, id=kwargs.get('pk', ''))
        shop_slug = request.POST.get('shop_slug', '')
        order = cart.simpleorder
        shop = get_object_or_404(Shop, slug=shop_slug)
        if order and flag:
            if flag == 'confirm':
                order.rejected_shops.remove(shop)
                order.confirm_shops.add(shop)
                order.save()
                return JsonResponse({'status': 0, 'message': 'Заказ успешно подтвержден.'})
            else:
                order.confirm_shops.remove(shop)
                order.rejected_shops.add(shop)
                order.save()
                return JsonResponse({'status': 0, 'message': 'Заказ отклонен.'})
        return JsonResponse({'status': 1, 'message': 'Заказ не найден.'})


