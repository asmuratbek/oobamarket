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
    help = "Parse products from www.optovik.kg"

    def handle(self, *args, **options):
        url = "http://www.optovik.kg/"
        html = requests.get(url + "products").content
        soup = BeautifulSoup(html, 'lxml')
        pagination = soup.find("div", class_="bx_pagination_page")
        max_page = pagination.find_all("li", class_=None)[-1].string
        products_links = list()
        [products_links.append(url + a.get("href")) for a in soup.find_all("a", class_="image_product")]
        wb = Workbook(encoding="utf-8")
        products_list = wb.add_sheet(u"Товары", cell_overwrite_ok=True)
        for page in range(2, int(max_page) + 1):
            page_html = requests.get("{}products?page={}".format(url, page)).content
            page_soup = BeautifulSoup(page_html, "lxml")
            [products_links.append(url + a.get("href")) for a in page_soup.find_all("a", class_="image_product")]
        for l, product in enumerate(products_links):
            prod_html = requests.get(product).content
            prod_soup = BeautifulSoup(prod_html, "lxml")
            prod_content = prod_soup.find("div", class_="bx_content_section")
            if prod_content and product.split("/")[-1] != "":
                title = prod_content.find("h1").string
                images_div = prod_content.find("div", class_="bx_item_slider")
                images = ",".join([a.get("href") for a in images_div.find_all("a")]) if images_div else ""
                available = "Есть" if int(prod_content.find("p", class_="avalible").find("span").string) > 0 else "Нет"
                price = prod_content.find("span", class_="pr").string
                code = ""
                short_desc = ""
                variables = ""
                slug = slugify(title) + "-optovik-" + str(l)
                desc = prod_content.find("div", class_="item_info_section")
                if not desc:
                    desc = ""
                product_fields = [title, code, short_desc, str(price), variables, available, images, str(slug), str(desc)]
                endrange = 3 + len(product_fields)
                write_products = list(map(lambda r, c: products_list.write(l, c, r), product_fields,
                                          [c for c in range(3, endrange)]))
                self.stdout.write(self.style.SUCCESS("%s записан. По счету %s" % (title, str(l))))
        file_name = "optovik.xls"
        wb.save("dump/" + file_name)
        self.stdout.write(self.style.SUCCESS("Done!"))
