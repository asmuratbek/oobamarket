from django import template
from django.utils.translation import ugettext_lazy as _

from apps.category.models import Category
from apps.global_category.models import GlobalCategory
from apps.meta.models import MetaData

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
        if isinstance(object, GlobalCategory):
            seo_data = MetaData.objects.filter(global_category=object).first()
            if seo_data:
                return {
                    'title': seo_data.title,
                    'description': seo_data.description,
                    'keywords': seo_data.keywords,
                    'h1': seo_data.h1,
                    'seo_text': seo_data.seo_text
                }
            else:
                return {
                    'title': "Интернет магазины Бишкек. Открыть интернет магазин.",
                    'description': " Интернет магазины Бишкек.Вы можете создать интернет магазин.",
                    'keywords': "интернет магазин, бишкек, интернет магазины бишкеке, купить",
                    'h1': "Ооба интернет магазин",
                    'seo_text': "Ооба интернет магазин"
                }
        elif isinstance(object, Category):
            seo_data = MetaData.objects.filter(category=object).first()
            if seo_data:
                return {
                    'title': seo_data.title,
                    'description': seo_data.description,
                    'keywords': seo_data.keywords,
                    'h1': seo_data.h1,
                    'seo_text': seo_data.seo_text
                }
            else:
                return {
                    'title': "Интернет магазины Бишкек. Открыть интернет магазин.",
                    'description': " Интернет магазины Бишкек.Вы можете создать интернет магазин.",
                    'keywords': "интернет магазин, бишкек, интернет магазины бишкеке, купить",
                    'h1': "Ооба интернет магазин",
                    'seo_text': "Ооба интернет магазин"
                }
        else:
            return {
                'title': "Интернет магазины Бишкек. Открыть интернет магазин.",
                'description': " Интернет магазины Бишкек.Вы можете создать интернет магазин.",
                'keywords': "интернет магазин, бишкек, интернет магазины бишкеке, купить",
                'h1': "Ооба интернет магазин",
                'seo_text': "Ооба интернет магазин"
            }

    return data
