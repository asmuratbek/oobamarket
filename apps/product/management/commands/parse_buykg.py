import requests, http.client, itertools
import urllib.request
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from django.http import Http404
from slugify import slugify
from xlwt import Workbook
from apps.product.models import Product


class Command(BaseCommand):
    help = "Parse products from www.buy.kg"

    def handle(self, *args, **options):
        url = 'http://buy.kg/item/'
        count = 0
        l = 0
        wb = Workbook(encoding="utf-8")
        products_list = wb.add_sheet(u"Товары", cell_overwrite_ok=True)
        for i in itertools.count():
            l += 1
            resp = http.client.HTTPConnection("www.buy.kg")
            resp.request("HEAD", "/item/{}/".format(i))
            response_head = resp.getresponse()
            if response_head.status == 200:
                count = 0
                get_prod = Product.objects.filter(slug__endswith="buykg-{}".format(i))
                if not get_prod:
                    html = requests.get(url + str(i) + "/").content
                    soup = BeautifulSoup(html, 'lxml')
                    cats = soup.find('div', class_='breadCrumbs')
                    cats_links = cats.find_all('a')
                    cats_list = [a.next for a in cats_links][2:-1]
                    title = soup.find('h3', class_='title').next
                    code = soup.find('p', class_='tt').next.split(":")[1].replace(' ', '')
                    short_desc = soup.find('p', class_='tt').next_sibling.next_sibling.next.replace("\r\n", "")
                    price = soup.find('p', class_='cost').next.split(" ")[0]
                    if price == "\n":
                        price = soup.find('p', class_='cost').find('span', class_="bold").next.split(" ")[0]
                    colors_div = soup.find("div", class_="colors")
                    color_spans = colors_div.find_all('span') if colors_div else None
                    colors_list = [span.get("style").split(":")[1] for span in color_spans] if color_spans else None
                    colors = ",".join(colors_list) if colors_list else "Не указано"
                    available = soup.find("span", class_="teal-text").next.next[1:]
                    images_div = soup.find("div", class_="owl-carousel").find_all("img")
                    image_links = ["http://buy.kg" + img.get("src") for img in images_div]
                    images = ",".join(image_links)
                    slug = slugify(title) + "-buykg-" + str(i)
                    description = soup.find("div", class_="description")
                    product_fields = [title, code, short_desc, price, colors, available, images, str(slug),
                                      str(description)]
                    endrange = 3 + len(product_fields)
                    write_cats = list(
                        map(lambda r, c: products_list.write(l, c, r), cats_list, [c for c in range(len(cats_list))]))
                    write_products = list(
                        map(lambda r, c: products_list.write(l, c, r), product_fields, [c for c in range(3, endrange)]))
                    self.stdout.write(self.style.SUCCESS("%s записан." % title))
                else:
                    self.stdout.write(self.style.SUCCESS("Товар уже существует."))
            else:
                count += 1
                self.stdout.write(self.style.ERROR(" Нет такой страницы 404"))
            if count >= 200:
                break
        file_name = "buykg_products.xls"
        wb.save("dump/" + file_name)
        self.stdout.write(self.style.SUCCESS("Done!"))

