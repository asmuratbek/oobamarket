import requests, http.client, itertools
import urllib.request
from functools import reduce
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from django.http import Http404
from django.utils.html import strip_tags
from slugify import slugify
from xlwt import Workbook


class Command(BaseCommand):
    help = "Parser products from penguin.kg"

    def handle(self, *args, **options):
        url = "https://penguin.kg/"
        l = 0
        html = requests.get(url).content
        soup = BeautifulSoup(html, "lxml")
        cats_div = soup.find("div", class_="col-md-3 hidden-sm-down")
        cats_list = cats_div.findAll("li", class_="block-nav__item")
        cats_list.pop(0)
        cats_list.pop(13)
        cats_list.pop(14)
        wb = Workbook(encoding="utf-8")
        products_list = wb.add_sheet(u"Товары", cell_overwrite_ok=True)
        cats_links = []
        for cat in cats_list:
            droplist = cat.find("ul", class_="droplist").findAll("li", class_="droplist__item")
            if droplist:
                [cats_links.append(li.find("a").get("href"))
                 for li in droplist if li.find("a").get("href").endswith("products")]
            else:
                cats_links.append(cat.find("a").get("href")) if cat.find("a").get("href").endswith("products") else None
        reduce(lambda r, c: r+c, cats_links)
        for link in cats_links:
            page_html = requests.get(link).content
            page_soup = BeautifulSoup(page_html, "lxml")
            div_row = page_soup.find("div", class_="loadarea").find("div", class_="section__item col-sm-12 col-md-9")\
                .find("div", class_="row")
            breadcrumbs = page_soup.find("ul", class_="breadcrumbs").findAll("li", class_="breadcrumbs__item")
            if breadcrumbs and len(breadcrumbs) > 2:
                categories = [str(cat_li.find("a").string).strip() for cat_li in breadcrumbs[2:]]
            if div_row:
                item_links = [i.find("a", class_="card__link").get("href")
                              for i in div_row.findAll("div", class_="col-sm-6 col-md-6 col-lg-3")]
                for item_link in item_links:
                    l += 1
                    item_html = requests.get(item_link).content
                    item_soup = BeautifulSoup(item_html, "lxml")
                    item_div = item_soup.find("div", class_="col-lg-8")
                    image_div = item_div.find("div", class_="col-md-6 col-lg-5")
                    image_list = image_div.findAll("img")
                    images = ",".join([img.get("src") for img in image_list]) if image_list else ""
                    content_div = item_div.find("div", class_="col-md-6 col-lg-7")\
                                            .find("div", class_="card card--item card--large")
                    if content_div:
                        title = content_div.get("data-item-prod_name", "")
                        code = content_div.get("data-item-barcode", "")
                        price = content_div.get("data-item-price", "")
                        short_desc = ""
                        vars = ""
                        available = "Есть"
                        slug = slugify(title) + "-penguin-" + str(l)
                        desc = item_div.find("div", class_="col-xs-12 col-md-6 col-lg-12")
                        product_fields = [title, code, short_desc, price, vars, available, images, str(slug), str(desc)]
                        endrange = 3 + len(product_fields)
                        write_cats = list(
                            map(lambda r, c: products_list.write(l, c, r), categories,
                                [c for c in range(len(categories))]))
                        write_products = list(
                            map(lambda r, c: products_list.write(l, c, r), product_fields,
                                [c for c in range(3, endrange)]))
                        self.stdout.write(self.style.SUCCESS("%s записан. По счету %s" % (title, str(l))))
        file_name = "penguin.xls"
        wb.save("dump/" + file_name)
        self.stdout.write(self.style.SUCCESS("Done!"))




