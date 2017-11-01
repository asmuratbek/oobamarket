from django.http import Http404
from django.shortcuts import get_object_or_404

from apps.cart.models import Cart
from apps.users.models import User


class CartOwnerUsers(object):
    def dispatch(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, id=kwargs.get('pk', ''))
        user = cart.user
        if request.method == 'GET':
            moders = list(User.objects.filter(is_staff=True))
            users_list = [user for item in cart.cartitem_set.all()
                          for user in item.product.shop.user.all()]
            users_list.append(user)
            users_list += moders
        else:
            users_list = [user]
        if request.user not in users_list:
            raise Http404
        return super(CartOwnerUsers, self).dispatch(request, *args, **kwargs)
