from django.http import HttpResponseRedirect
from django.urls import reverse

from apps.shop.models import Shop


class AddProductMixin(object):

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        shop = Shop.objects.filter(user__id__in=[user.id]).first()
        if not shop:
            return HttpResponseRedirect(reverse('shops:create'))
        my_shop = user.shop_set.filter(slug=self.kwargs.get('slug', None))

        if not my_shop:
            return HttpResponseRedirect(reverse('product:add_product', kwargs={'slug': shop.slug}))
        return super(AddProductMixin, self).dispatch(request, *args, **kwargs)
