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
    help = "Parse products from www.yvesrocher.kg"

    def handle(self, *args, **options):
        url = "http://yvesrocher.kg/obzor-kategorij/"
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'lxml')
        cats_block = soup.find("div", class_="products-block")
        cats_list = cats_block.findAll('div', class_="product-category")
        cats_links = [cat.find("a").get("href") for cat in cats_list]
        product_links = list()
        other_pages = list()
        wb = Workbook(encoding="utf-8")
        products_list = wb.add_sheet(u"Товары", cell_overwrite_ok=True)
        for cat in cats_links:
            cat_html = requests.get(cat).content
            cat_soup = BeautifulSoup(cat_html, 'lxml')
            pagination = cat_soup.find("nav", class_="paging")
            if pagination:
                max_page = pagination.findAll("li")[-2].find("a", class_="page-numbers").string
                if int(max_page) != 2:
                    pages = [other_pages.append(cat + "page/" + str(i) + "/")
                             for i in range(2, int(max_page) + 1)]
                else:
                    other_pages.append(cat + "page/2/")
            products_block = cat_soup.find("div", class_="products-block")
            products = products_block.findAll("div", class_="product-col")
            [product_links.append(div.find("a", class_="product-image").get("href")) for div in products]
        for page in other_pages:
            page_html = requests.get(page).content
            page_soup = BeautifulSoup(page_html, 'lxml')
            products_block = page_soup.find("div", class_="products-block")
            products = products_block.findAll("div", class_="product-col")
            [product_links.append(div.find("a", class_="product-image").get("href")) for div in products]
        for l, product in enumerate(product_links):
            try:
                prod_html = requests.get(product).content
            except requests.ConnectionError:
                continue
            prod_soup = BeautifulSoup(prod_html, 'lxml')
            title = prod_soup.find("h1", class_="product_title")
            if title:
                title = title.string
                price_block = prod_soup.find("p", class_="price")
                if price_block:
                    ins = price_block.find("ins")
                    if ins:
                        price = ins.find("span").next
                    else:
                        price = price_block.find("span", class_="woocommerce-Price-amount").next
                else:
                    price = 0
                image_div = prod_soup.find("div", class_="images")
                images = ",".join([img.get("src") for img in image_div.findAll("img")])
                desc = prod_soup.find("div", class_="description")
                if not desc:
                    desc = ""
                slug = slugify(title) + "-yvesrocher-" + str(l)
                code = ""
                short_desc = ""
                variables = ""
                available = "Есть"
                product_fields = [title, code, short_desc, str(price), variables, available, images, str(slug), str(desc)]
                endrange = 3 + len(product_fields)
                write_products = list(map(lambda r, c: products_list.write(l, c, r), product_fields,
                                          [c for c in range(3, endrange)]))
                self.stdout.write(self.style.SUCCESS("%s записан. По счету %s" % (title, str(l))))
            else:
                continue
        file_name = "yvesrocher.xls"
        wb.save("dump/" + file_name)
        self.stdout.write(self.style.SUCCESS("Done!"))
