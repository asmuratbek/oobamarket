from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from apps.product.models import Product
from apps.shop.models import Shop


@csrf_exempt
def counter(request):
    if request.method == 'POST' and request.is_ajax:
        slug = request.POST.get('slug', '')
        try:
            item = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            item = get_object_or_404(Shop, slug=slug)
        item.counter += 1
        item.save()
        return HttpResponse('Success')
    return HttpResponse('Error')
