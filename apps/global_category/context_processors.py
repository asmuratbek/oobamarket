from .models import GlobalCategory
from django.conf import settings


def fixed_categories(request):
    return {
        'fixed_categories': GlobalCategory.objects.filter(published=True),
    }


def domain_url(request):
    return {
        'DOMAIN_URL': settings.DOMAIN_URL
    }
