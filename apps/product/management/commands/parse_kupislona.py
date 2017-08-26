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
    help = "Parse products from www.kupislona.kg"

    def handle(self, *args, **options):
        url = "http://kupislona.kg"
        html = requests.get(url).content
        soup = BeautifulSoup(html, "lxml")
        nav_bar = soup.find("ul", class_="nav navbar-nav")
        dropdowns = nav_bar.findAll("li")
        # all_cats = [url + li.find("a").get("href") for cat in dropdowns
        #             if cat.find("ul", class_="dropdown-menu")
        #             for li in cat.find("ul", class_="dropdown-menu").findAll("li")]
        all_cats = [url + cat.find("a").get("href") for cat in dropdowns
                    if not cat.find("ul", class_="dropdown-menu")]
        other_pages = list()
        product_links = list()
        wb = Workbook(encoding="utf-8")
        products_list = wb.add_sheet(u"Товары", cell_overwrite_ok=True)
        for cat in all_cats:
            cat_html = requests.get(cat).content
            cat_soup = BeautifulSoup(cat_html, "lxml")
            pagination = cat_soup.find("nav", class_="paginationBlock")
            if pagination:
                page_nums = pagination.findAll("li")
                page_nums.pop(0), page_nums.pop(-1)
                paginate_cats = [other_pages.append(url + page.find("a").get("href")) for page in page_nums[1:]]
            products = [product_links.append(url + product.find("link", itemprop="url").get("href"))
                        for product in cat_soup.findAll("div", itemprop="itemListElement")]
        for other_cat in other_pages:
            other_html = requests.get(other_cat).content
            other_soup = BeautifulSoup(other_html, 'lxml')
            products = [product_links.append(url + product.find("link", itemprop="url").get("href"))
                        for product in other_soup.findAll("div", itemprop="itemListElement")]
        for l, prod in enumerate(product_links):
            prod_html = requests.get(prod).content
            prod_soup = BeautifulSoup(prod_html, 'lxml')
            title = prod_soup.find("h3", class_="title").string
            image_box = prod_soup.find("div", class_="smallImgBox")
            images = ",".join([img.find("a").get("href")
                               for img in image_box.findAll("div", class_="smallImg")]) if image_box else ""
            price_div = prod_soup.find("div", class_="formShop")
            price_str = price_div.find("h3").find("span", class_="fixPrice") if price_div else "0"
            if not price_str:
                price_str = price_div.find("h3").find("span", class_="newPrice").string
            price = re.findall('\d+', str(price_str))[0]
            code = ""
            short_desc = ""
            variables = ""
            available = "Есть"
            slug = slugify(title) + "-kupislona-" + str(l)
            desc = prod_soup.find("div", id="desc")
            if not desc:
                desc = ""
            product_fields = [title, code, short_desc, str(price), variables, available, images, str(slug), str(desc)]
            endrange = 3 + len(product_fields)
            write_products = list(map(lambda r, c: products_list.write(l, c, r), product_fields,
                                [c for c in range(3, endrange)]))
            self.stdout.write(self.style.SUCCESS("%s записан. По счету %s" % (title, str(l))))
        file_name = "kupislona.xls"
        wb.save("dump/" + file_name)
        self.stdout.write(self.style.SUCCESS("Done!"))
