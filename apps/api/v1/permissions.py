from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    message = "You must be the owner of this Post"

    def has_object_permission(self, request, view, obj):
        return obj.shop.is_owner(request.user)
