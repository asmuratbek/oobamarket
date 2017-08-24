import requests
import urllib.request
from functools import reduce
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from django.http import Http404
from django.utils.html import strip_tags
from slugify import slugify
from xlwt import Workbook


class Command(BaseCommand):
    help = "Parser products from www.stroymag-bishkek.kg"

    def handle(self, *args, **options):
        url = "https://www.stroymag-bishkek.com/shop/page/{page}/?s"
        html = requests.get(url.format(page=1)).content
        soup = BeautifulSoup(html, "lxml")
        page_list = soup.find("nav", class_="page-nav").findAll("li")
        max_pages = int(page_list[-2].find("a").string) + 1
        wb = Workbook(encoding="utf-8")
        products_list = wb.add_sheet(u"Товары", cell_overwrite_ok=True)
        l = 0
        for page in range(1, max_pages):
            page_html = requests.get(url.format(page=page)).content
            page_soup = BeautifulSoup(page_html, 'lxml')
            content_div = page_soup.find("div", class_="art_details")
            product_div = content_div.find("div", class_="article")
            if product_div:
                product_list = product_div.findAll("a", class_="woocommerce-LoopProduct-link")
                products_links = [link.get("href") for link in product_list]
                for product in products_links:
                    product_html = requests.get(product).content
                    product_soup = BeautifulSoup(product_html, "lxml")
                    categories = [cat.find("a").string
                                  for cat in product_soup.find("ul", class_="breadcrumbs").findAll("li")
                                  if cat.find("a")][2:]
                    product_content = product_soup.find("div", class_="art_details")
                    if product_content:
                        prod_details = product_content.find("div", class_="cart_details")
                        product_upper = prod_details.find("div", class_="cart_upper")
                        image = product_upper.find("div", class_="imgHldr").find("a", class_="woocommerce-main-image").get("href")
                        title = product_upper.find("div", class_="txtHldr").find("h2", class_="product_title").string
                        code = ""
                        price_p = product_upper.find("p", class_="offer-price")
                        price = str(price_p.find("span", class_="woocommerce-Price-amount").next).replace(",", "") \
                            if price_p else ""
                        short_desc = ""
                        available = "Есть"
                        slug = slugify(title) + "-stroymag-" + str(l)
                        variables = ""
                        desc = product_upper.find("div", itemprop="description")
                        prod_lower = prod_details.find("div", class_="descript")
                        desc2 = prod_lower.find("div", id="tabone")
                        if desc2 and desc:
                            new_tag = product_soup.new_tag("p")
                            new_tag.string = desc2.string if desc2.string else ""
                            desc.append(new_tag)
                        product_fields = [title, code, short_desc, price, variables, available, image, str(slug), str(desc)]
                        endrange = 3 + len(product_fields)
                        write_cats = list(
                            map(lambda r, c: products_list.write(l, c, r), categories,
                                [c for c in range(len(categories))]))
                        write_products = list(
                            map(lambda r, c: products_list.write(l, c, r), product_fields,
                                [c for c in range(3, endrange)]))
                        l += 1
                        self.stdout.write(self.style.SUCCESS("%s записан. По счету %s" % (title, str(l))))
        file_name = "stroymag.xls"
        wb.save("dump/" + file_name)
        self.stdout.write(self.style.SUCCESS("Done!"))



