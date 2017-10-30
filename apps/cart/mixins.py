from django.http import Http404
from django.shortcuts import get_object_or_404

from apps.cart.models import Cart


class CartOwnerUsers(object):
    def dispatch(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, id=kwargs.get('pk', ''))
        user = cart.user
        users_list = [user for item in cart.cartitem_set.all()
                      for user in item.product.shop.user.all()]
        users_list.append(user)
        if request.user not in users_list:
            raise Http404
        return super(CartOwnerUsers, self).dispatch(request, *args, **kwargs)
