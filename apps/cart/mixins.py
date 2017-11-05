from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from apps.cart.models import Cart
from apps.shop.models import Shop
from apps.users.models import User


class CartOwnerUsers(object):
    def dispatch(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, id=kwargs.get('pk', ''))
        user = cart.user
        moders = list(User.objects.filter(is_staff=True))
        if request.method == 'GET':
            users_list = [user for item in cart.cartitem_set.all()
                          for user in item.product.shop.user.all()]
            users_list.append(user)
            users_list += moders
        else:
            moders.append(user)
            users_list = moders
        if request.user not in users_list:
            raise Http404
        return super(CartOwnerUsers, self).dispatch(request, *args, **kwargs)


class ConfirmOrderByShopOwner(object):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        moders = User.objects.filter(is_staff=True)
        shop_slug = request.POST.get('shop_slug', '')
        shop = get_object_or_404(Shop, slug=shop_slug)
        users_list = list(shop.user.all()) + list(moders)
        if user not in users_list:
            raise HttpResponseBadRequest
        return super(ConfirmOrderByShopOwner, self).dispatch(request, *args, **kwargs)
