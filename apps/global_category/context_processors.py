import math
from itertools import zip_longest

from .models import GlobalCategory
from django.conf import settings


def fixed_categories(request):
    global_cats = GlobalCategory.objects.filter(published=True)
    center_index = math.ceil(global_cats.count() / 2)
    first_col = global_cats[:center_index]
    second_col = global_cats[center_index:]
    return {
        'fixed_categories': global_cats,
        'footer_cats': [first_col, second_col]
    }


def domain_url(request):
    return {
        'DOMAIN_URL': settings.DOMAIN_URL
    }
