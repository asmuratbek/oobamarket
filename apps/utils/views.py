import imghdr, os

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from apps.product.models import Product, ProductImage
from apps.shop.models import Shop
from django.conf import settings


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


def change_format():
    images = ProductImage.objects.all()
    for image in images:
        try:
            valid_format = imghdr.what(image.image.path)
        except FileNotFoundError:
            continue
        if valid_format:
            if not image.image.name.endswith(valid_format):
                new_name = str(image.image.name).replace(".jpg", "." + valid_format)
                os.rename(image.image.path, settings.MEDIA_ROOT + "/" + new_name)
                image.image.name = new_name
                image.save()
                print("{} изменен".format(new_name))
    print("Done")


def create_thumbnails():
    products = Product.objects.all()
    for product in products:
        avatar_image = product.productimage_set.filter(is_avatar=True).first()
        first_image = product.productimage_set.first()
        if product.productimage_set.all():
            if avatar_image:
                try:
                    avatar_image.save()
                except Exception:
                    continue
                name = os.path.split(avatar_image.thumb_image.name)[-1]
            else:
                try:
                    first_image.create_thumbnail()
                    first_image.save()
                except Exception:
                    continue
                name = os.path.split(first_image.thumb_image.name)[-1]
            print("Миниатюра для {} создана.".format(name))
    print("Done!")
