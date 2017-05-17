from django.http import HttpResponseRedirect
from django.urls import reverse

from apps.shop.models import Shop


class AddProductMixin(object):

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        shop = Shop.objects.filter(user__id__in=[user.id]).first()
        if not shop:
            return HttpResponseRedirect(reverse('shops:create'))
        return super(AddProductMixin, self).dispatch(request, *args, **kwargs)
