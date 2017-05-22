from django import template
from django.utils.translation import ugettext_lazy as _

from apps.meta.models import MetaData
from apps.product.models import Product
from apps.shop.models import Shop

register = template.Library()


@register.assignment_tag()
def get_seo_data(request, object):
    data = {'seo_text': ''}
    try:
        seo_data = MetaData.objects.get(url=request.get_full_path())
        if seo_data:
            return {
                'title': seo_data.title,
                'description': seo_data.description,
                'keywords': seo_data.keywords,
                'h1': seo_data.h1,
                'seo_text': seo_data.seo_text
            }


    except MetaData.DoesNotExist:
        if isinstance(object, Shop):
            seo_data = MetaData.objects.get(shop=object)
            return {
                'title': seo_data.title,
                'description': seo_data.description,
                'keywords': seo_data.keywords,
                'h1': seo_data.h1,
                'seo_text': seo_data.seo_text
            }
        elif isinstance(object, Product):
            print(object)
            seo_data = MetaData.objects.get(product=object)
            return {
                'title': seo_data.title,
                'description': seo_data.description,
                'keywords': seo_data.keywords,
                'h1': seo_data.h1,
                'seo_text': seo_data.seo_text
            }
        else:
            return {
                'title': "Ооба интеренет магазин",
                'description': "Ооба интеренет магазин",
                'keywords': "Ооба интеренет магазин",
                'h1': "Ооба интеренет магазин",
                'seo_text': "Ооба интеренет магазин"
            }

    return data
