import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from apps.product.models import ProductImage
from apps.shop.models import Shop


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('slug', nargs="+", type=str)

    def handle(self, *args, **options):
        shop_slug = options['slug'][0]
        shop = get_object_or_404(Shop, slug=shop_slug)
        images = os.listdir(settings.MEDIA_ROOT + "/products/image/")
        for product in shop.product_set.all():
            product_slug = "-".join(product.slug.lower().split("-")[:-1])
            images = [img for img in images if img.startswith(product_slug)]
            if images:
                [image.delete() for image in product.productimage_set.all()]
                [ProductImage.objects.create(product=product, image="products/image/" + img) for img in images]
                self.stdout.write(self.style.SUCCESS("Картинки для {} созданы.".format(product.title)))
        self.stdout.write(self.style.SUCCESS("Done!!!"))
