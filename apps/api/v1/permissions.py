from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    message = "You must be the owner of this Post"

    def has_object_permission(self, request, view, obj):
        return obj.shop.is_owner(request.user)


class IsUserOwner(BasePermission):
    message = "You must be the owner of this profile"

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.id == int(view.kwargs.get('pk')) if view.kwargs.get('pk') else None
        return False
