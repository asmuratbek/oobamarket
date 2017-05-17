from django.urls import reverse

from apps.shop.models import Shop


class AddProductMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        user.shop = Shop.objects.filter(user=user)
        if user.shop is None:
            return reverse('shops:create')
        if user.shop is not None:
            return reverse('product:add_product_index')
