from .models import GlobalCategory


def fixed_categories(request):
    return {
        'fixed_categories': GlobalCategory.objects.all(),
    }
