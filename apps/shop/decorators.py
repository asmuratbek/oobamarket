from django.http import Http404
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils.six import wraps

from apps.shop.models import Shop, Banners


def delete_decorator(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        shop_slug = request.POST.get('shop_slug', '')
        banner_id = request.POST.get('banner_id', '')
        if shop_slug and banner_id:
            user = request.user
            try:
                user_shop = user.shop_set.get(slug=shop_slug)
            except Shop.DoesNotExist:
                return Http404
            banner = get_object_or_404(Banners, id=banner_id)
            get_banner = [ban for ban in user_shop.banners_set.all() if ban == banner]
            if get_banner:
                return function(request, *args, **kwargs)
            else:
                return HttpResponseBadRequest
    return decorator
