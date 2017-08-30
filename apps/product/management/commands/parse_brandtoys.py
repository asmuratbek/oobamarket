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
    help = "Parse products from www.brandtoys.kg"

    def handle(self, *args, **options):
        url = "http://www.brandtoys.kg"
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'lxml')
        cats_ul = soup.find("ul", class_="vmenu")
        cats_li = cats_ul.findAll("li", class_='deeper')
        cats = [url + a.find("a").get("href") for li in cats_li
                    for a in li.find('ul').findAll('li')]
        other_cats = [url + li.find("a").get("href") for li in cats_ul.findAll('li')[-2:]]
        all_cats = cats + other_cats
        product_links = list()
        other_pages = list()
        wb = Workbook(encoding="utf-8")
        products_list = wb.add_sheet(u"Товары", cell_overwrite_ok=True)
        for cat in all_cats:
            cat_html = requests.get(cat).content
            cat_soup = BeautifulSoup(cat_html, 'lxml')
            pagination = cat_soup.find("div", class_="pagination")
            if pagination:
                pages = pagination.findAll("li", class_=None)
                [other_pages.append(url + a.find("a").get("href")) for a in pages if a.find("a")]
            products_block = cat_soup.find("div", class_="jshop_list_product")
            if products_block:
                [product_links.append(url + p.find("a").get("href"))
                                  for p in products_block.findAll("div", class_="image_block")]
        for page in other_pages:
            page_html = requests.get(page).content
            page_soup = BeautifulSoup(page_html, 'lxml')
            products_block = page_soup.find("div", class_="jshop_list_product")
            if products_block:
                [product_links.append(url + p.find("a").get("href"))
                                  for p in products_block.findAll("div", class_="image_block")]
        for l, product in enumerate(product_links):
            prod_html = requests.get(product).content
            prod_soup = BeautifulSoup(prod_html, 'lxml')
            product_content = prod_soup.find("form", attrs={"name": "product"})
            title = product_content.find("h1").string
            images_block = product_content.find("td", class_="jshop_img_description")
            images = ",".join([img.get("src")
                               for img in images_block.findAll("img", class_="jshop_img_thumb")]) if images_block else ""
            if images == "":
                images = product_content.find("td", class_="image_middle").find("a").get("href")
            desc = product_content.find("div", class_="description")
            price_div = product_content.find("div", class_="prod_price")
            if price_div:
                price_str = price_div.find("span", id="block_price").string
                price = re.findall('\d+', str(price_str))[0]
            else:
                price = ""
            code = ""
            short_desc = ""
            variables = ""
            available = "Есть"
            slug = slugify(title) + "-brandtoys-" + str(l)
            product_fields = [title, code, short_desc, str(price), variables, available, images, str(slug), str(desc)]
            endrange = 3 + len(product_fields)
            write_products = list(map(lambda r, c: products_list.write(l, c, r), product_fields,
                                [c for c in range(3, endrange)]))
            self.stdout.write(self.style.SUCCESS("%s записан. По счету %s" % (title, str(l))))
        file_name = "brandtoys.xls"
        wb.save("dump/" + file_name)
        self.stdout.write(self.style.SUCCESS("Done!"))




