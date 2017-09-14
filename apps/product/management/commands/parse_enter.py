import requests, re
import urllib.request
from functools import reduce
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from django.http import Http404
from django.utils.html import strip_tags
from slugify import slugify
from xlwt import Workbook


class Command(BaseCommand):
    help = "Parse products from www.enter.kg"

    def handle(self, *args, **options):
        url = "http://enter.kg"
        cats_url = url + "/virtuemart-categories"
        html = requests.get(cats_url).content
        soup = BeautifulSoup(html, "lxml")
        product_links = list()
        wb = Workbook(encoding="utf-8")
        products_list = wb.add_sheet(u"Товары", cell_overwrite_ok=True)
        pages = soup.find("span", class_="vm-page-counter").string
        max_page = re.findall("\d+", pages)[-1]
        [product_links.append(url + s.find("a").get("href"))
         for s in soup.find_all("span", class_="prouct_name")]
        for i in range(1, int(max_page)):
            page_html = requests.get(cats_url + "?start={}00".format(i)).content
            page_soup = BeautifulSoup(page_html, "lxml")
            [product_links.append(url + s.find("a").get("href"))
             for s in page_soup.find_all("span", class_="prouct_name")]
            self.stdout.write(self.style.SUCCESS("Лист {} добавлен.".format(i)))
        for l, product in enumerate(product_links):
            prod_html = requests.get(product).content
            prod_soup = BeautifulSoup(prod_html, "lxml")
            title = str(prod_soup.find("span", class_="prouct_name").string).strip()
            short_desc = ""
            code = ""
            variables = ""
            image_div = prod_soup.find("div", class_="main-image")
            image_a = image_div.find("a", rel="vm-additional-images") if image_div else ""
            images = url + str(image_a.get("href")) if image_a != "" and "www.google" not in str(image_a.get("href")) else ""
            price_span = prod_soup.find("span", class_="price")
            price = re.findall("\d+", str(price_span.string).split("/")[0])[0] if price_span else 0
            slug = slugify(title) + "-enter-" + str(l)
            desc = ""
            available = "Есть"
            product_fields = [title, code, short_desc, str(price), variables, available, str(images), str(slug), str(desc)]
            endrange = 3 + len(product_fields)
            write_products = list(map(lambda r, c: products_list.write(l, c, r), product_fields,
                                      [c for c in range(3, endrange)]))
            self.stdout.write(self.style.SUCCESS("%s записан. По счету %s" % (title, str(l))))
        file_name = "enter.xls"
        wb.save("dump/" + file_name)
        self.stdout.write(self.style.SUCCESS("Done!"))


