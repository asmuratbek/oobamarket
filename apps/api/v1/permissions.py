from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from apps.cart.models import Cart
from apps.product.models import Product

from apps.shop.models import Shop, Sales
from apps.users.models import User

from django.db.models import Q


class IsOwnerOrReadOnly(BasePermission):
    message = "You must be the owner of this Post"

    def has_object_permission(self, request, view, obj):
        return obj.shop.is_owner(request.user)


class IsOwnerShop4Product(BasePermission):
    message = "You must be owner of shop"

    def has_permission(self, request, view):
        if request.method == 'POST' or request.method == 'PUT':
            user = request.user
            # shop = get_object_or_404(Shop, slug=request.data.get("shop", ""))
            shop = get_object_or_404(Shop, slug=request.data.get("shop", ""))
            return user in shop.user.all()
        return True


class IsNotOwnerShop(BasePermission):
    message = "You must be not owner of shop"

    def has_permission(self, request, view):
        shop = get_object_or_404(Shop, slug=request.data.get('shop', ''))
        user = request.user
        return user not in shop.user.all()


class IsOwnerShop4Shop(BasePermission):
    message = "You must be owner of shop"

    def has_permission(self, request, view):
        shop = get_object_or_404(Shop, slug=view.kwargs['slug'])
        user = request.user
        return user in shop.user.all()


class IsSaleOfShop(BasePermission):
    message = "Sale must be of shop."

    def has_permission(self, request, view):
        shop = get_object_or_404(Shop, slug=view.kwargs.get('slug'))
        sale = get_object_or_404(Sales, pk=view.kwargs.get('pk'))
        return sale.shop == shop


class IsUserOwner(BasePermission):
    message = "You must be the owner of this profile"

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.id == int(view.kwargs.get('pk')) if view.kwargs.get('pk') else None
        return False


class IsOwnerOfProduct(BasePermission):
    message = 'You must be the owner of this product'

    def has_permission(self, request, view):
        product = get_object_or_404(Product, slug=view.kwargs.get('slug'))
        return request.user in product.shop.user.all()


class CartHistoryPerm(BasePermission):
    message = 'You must be owner of cart or owner of shop in cart or moderator'

    def has_permission(self, request, view):
        if request.method == 'GET':
            cart = get_object_or_404(Cart, id=view.kwargs.get('pk'))
            users = list(User.objects.filter(Q(id__in=cart.get_shops().values_list('user', flat=True))|Q(is_staff=True)))
            users.append(cart.user)
            return request.user in users
        else:
            cart = get_object_or_404(Cart, id=view.kwargs.get('pk'))
            flag = request.data.get('flag')
            if flag:
                if flag == 'shop':
                    users = list(User.objects.filter(Q(id__in=cart.get_shops().values_list('user', flat=True)) |
                                                     Q(is_staff=True)))
                    return request.user in users
                elif flag == 'user':
                    users = list(User.objects.filter(is_staff=True))
                    users.append(cart.user)
                    return request.user in users
                else:
                    return False
            return False
