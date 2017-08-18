import requests, json
import urllib.request
from django.core.management.base import BaseCommand
from django.http import Http404
from slugify import slugify
from xlwt import Workbook
from functools import reduce


class Command(BaseCommand):
    help = "Parser from alliance.kg"

    def handle(self, *args, **options):
        url = "http://176.126.167.121:8002/"
        response = requests.get(url).json()
        all_cats = reduce(lambda r,c: r + c, [cat['categories'] for cat in response['data']['global_categories']])
        cat_urls = [(url + "product-category/" + str(cat['id']) + "/", str(cat['title'])) for cat in all_cats]
        wb = Workbook(encoding="utf-8")
        products_list = wb.add_sheet(u"Товары", cell_overwrite_ok=True)
        l = 0
        for cat_url, cat_title in cat_urls:
            cat_resp = requests.get(cat_url).json()
            products = cat_resp['data']['products']
            for product in products:
                l += 1
                title = product['name']
                code = product.get("barcode", "")
                short_desc = ""
                price = product['price']
                vars = ""
                image = product.get("image", "")
                slug = slugify(title) + "-alliance-" + str(l)
                active = product["is_active"]
                available = "Есть" if active else "Нет"
                desc = product["description"]
                product_list = [title, code, short_desc, price, vars, available, image, str(slug), str(desc)]
                endrange = 3 + len(product_list)
                write_cats = products_list.write(l, 0, cat_title)
                write_products = list(
                    map(lambda r, c: products_list.write(l, c, r), product_list, [c for c in range(3, endrange)]))
                self.stdout.write(self.style.SUCCESS("%s записан. По счету - %s" % (title, l)))
        file_name = "alliance.xls"
        wb.save("dump/" + file_name)
        self.stdout.write(self.style.SUCCESS("Done!"))



