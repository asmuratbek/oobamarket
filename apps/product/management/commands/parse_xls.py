import os, xlrd, urllib.request
from django.conf import settings
from django.core.management.base import BaseCommand
from apps.shop.models import Shop
from apps.product.models import Product, ProductImage
from apps.category.models import Category
from decimal import Decimal


class Command(BaseCommand):
    help = "Parse products from xls file in dump directory"

    def add_arguments(self, parser):
        parser.add_argument('file_name', nargs='+', type=str)
        parser.add_argument('shop_slug', nargs='+', type=str)
        parser.add_argument('cat_slug', nargs='+', type=str)

    def handle(self, *args, **options):
        file_name = options['file_name'][0]
        shop_slug = options['shop_slug'][0]
        cat_slug = options['cat_slug'][0]
        dump_dir = os.listdir(str(settings.DUMP_ROOT))
        file = [f for f in dump_dir if f == str(file_name)]
        if not file:
            return self.stdout.write(self.style.ERROR("Файл в папке dump не найден."))
        try:
            shop = Shop.objects.get(slug=shop_slug)
        except Shop.DoesNotExist:
            return self.stdout.write(self.style.ERROR("Магазин не найден"))
        try:
            category = Category.objects.get(slug=cat_slug)
        except Category.DoesNotExist:
            return self.stdout.write(self.style.ERROR("Категория не найдена"))
        wb = xlrd.open_workbook(settings.DUMP_ROOT + "/" + file_name)
        sheet = wb.sheet_by_index(0)
        data = [[sheet.cell_value(r, c) for c in range(3, sheet.ncols)] for r in range(sheet.nrows) if \
                sheet.row(r)[3].value != ""]
        for product in data:
            slug = product[7].lower() if len(product[7]) <= 255 else product[7].lower()[:255]
            price = Decimal(product[3]) if product[3] != "" else 0
            title = product[0]
            short_desc = product[2]
            active = str(product[5])
            available = 'available' if active.startswith("Есть") else "not_available"
            desc = product[8]
            try:
                prod = Product.objects.get(slug=slug)
                if prod:
                    prod.price = price
                    prod.title = title
                    prod.short_description = short_desc
                    prod.availability = available
                    prod.long_description = desc
                    prod.save()
                    self.stdout.write(self.style.SUCCESS("{} изменен.".format(title)))
            except Product.DoesNotExist:
                imgs_list = product[6].split(",")
                product_create = Product.objects.create(shop=shop, category=category, title=title, slug=slug,
                                                        price=price,
                                                        availability=available, short_description=short_desc,
                                                        long_description=desc)
                img_i = 0
                for img in imgs_list:
                    img_format = img[-4:].replace(".", "")
                    img_i += 1
                    try:
                        download_imgs = urllib.request.urlretrieve(img, settings.MEDIA_ROOT + "/products/image/" +
                                                                    str(slug) + "-{}.{}".format(img_i, img_format))
                        product_images = ProductImage.objects.create(product=product_create, image="products/image/" + str(slug) +
                                                                                                   "-{}.{}".format(img_i,
                                                                                                                   img_format))
                    except ValueError:
                        continue
                    except urllib.request.URLError:
                        continue
                self.stdout.write(self.style.SUCCESS("{} создан.".format(title)))
        return self.stdout.write(self.style.SUCCESS("Done!"))
