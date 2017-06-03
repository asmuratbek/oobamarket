from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse

from apps.product.models import Product
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


class UpdateProductMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        my_product = get_object_or_404(Product, slug=kwargs.get('slug'))
        my_shop = user.shop_set.all()
        if my_product.shop not in my_shop:
            return HttpResponseForbidden()
        return super(UpdateProductMixin, self).dispatch(request, *args, **kwargs)



class DeleteProductMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        product = get_object_or_404(Product, slug=self.kwargs.get('slug'))
        if not user in product.shop.user.all():
            return HttpResponseForbidden()

        return super(DeleteProductMixin, self).dispatch(request, *args, **kwargs)


class AddBannerMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        shop = Shop.objects.filter(user__id__in=[user.id]).first()
        if not shop:
            return HttpResponseRedirect(reverse('shops:create'))
        my_shop = user.shop_set.filter(slug=self.kwargs.get('slug', None))

        if not my_shop:
            return HttpResponseRedirect(reverse('shops:detail', kwargs={'slug': shop.slug}))
        return super(AddBannerMixin, self).dispatch(request, *args, **kwargs)


class AddSocialLinksMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        shop = Shop.objects.filter(user__id__in=[user.id]).first()
        if not shop:
            return HttpResponseRedirect(reverse('shops:create'))
        my_shop = user.shop_set.filter(slug=self.kwargs.get('slug', None))

        if not my_shop:
            return HttpResponseRedirect(reverse('shops:detail', kwargs={'slug': shop.slug}))
        return super(AddSocialLinksMixin, self).dispatch(request, *args, **kwargs)


class UpdateShopMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        shop = Shop.objects.filter(user__id__in=[user.id]).first()
        if not shop:
            return HttpResponseRedirect(reverse('shops:create'))
        my_shop = user.shop_set.filter(slug=self.kwargs.get('slug', None))

        if not my_shop:
            return HttpResponseForbidden()
        return super(UpdateShopMixin, self).dispatch(request, *args, **kwargs)


class DeleteShopMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        shop = Shop.objects.filter(user__id__in=[user.id]).first()
        if not shop:
            return HttpResponseRedirect(reverse('shops:create'))
        my_shop = user.shop_set.filter(slug=self.kwargs.get('slug', None))

        if not my_shop:
            return HttpResponseForbidden()
        return super(DeleteShopMixin, self).dispatch(request, *args, **kwargs)
