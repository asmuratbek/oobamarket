from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from apps.shop.models import Shop


class IsOwnerOrReadOnly(BasePermission):
    message = "You must be the owner of this Post"

    def has_object_permission(self, request, view, obj):
        return obj.shop.is_owner(request.user)


class IsOwnerShop(BasePermission):
    message = "You must be owner of shop"

    def has_permission(self, request, view):
        if request.method == 'POST' or request.method == 'PUT':
            user = request.user
            # shop = get_object_or_404(Shop, slug=request.data.get("shop", ""))
            shop = get_object_or_404(Shop, slug=request.data.get("shop", ""))
            return user in shop.user.all()
        return True


class IsUserOwner(BasePermission):
    message = "You must be the owner of this profile"

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.id == int(view.kwargs.get('pk')) if view.kwargs.get('pk') else None
        return False
