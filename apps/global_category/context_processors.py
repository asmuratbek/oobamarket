from itertools import zip_longest

from .models import GlobalCategory
from django.conf import settings


def fixed_categories(request):
    global_cats = GlobalCategory.objects.filter(published=True)
    return {
        'fixed_categories': global_cats,
        'footer_cats': list(zip_longest(*[iter(global_cats)] * 3))
    }


def domain_url(request):
    return {
        'DOMAIN_URL': settings.DOMAIN_URL
    }
