import requests, http.client, itertools
import urllib.request
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from django.http import Http404
from django.utils.html import strip_tags
from slugify import slugify
from xlwt import Workbook


class Command(BaseCommand):
    help = "Parse products from www.bigser.kg"

    def handle(self, *args, **options):
        url = "http://bigser.kg/product/{id}"
        count = 0
        l = 0
        wb = Workbook(encoding="utf-8")
        products_list = wb.add_sheet(u"Товары", cell_overwrite_ok=True)
        for i in itertools.count():
            resp = http.client.HTTPConnection("bigser.kg")
            resp.request("HEAD", "/product/{}".format(i))
            response_head = resp.getresponse()
            if response_head.status == 200:
                l += 1
                count = 0
                html = requests.get(url.format(id=int(i))).content
                soup = BeautifulSoup(html, 'lxml')
                title = soup.find("div", class_="title").string
                if title != "" and title is not None:
                    code = soup.find("div", class_="article").find("span").string
                    variables = soup.find("div", class_="fabric").find("p")
                    if variables:
                        variables = strip_tags(variables.string)
                    price = soup.find("div", class_="site-price").find("span").string.split(" ")[0]
                    available = "Есть"
                    size = soup.find("div", class_="size").find("span")
                    if size:
                        size = size.string
                    color_list = soup.find("div", class_="colors").findAll("span")
                    colist = [span.string for span in color_list]
                    colors = ",".join(colist) if colist[0] != None else ""
                    desc = soup.find("div", class_="desc").find("div")
                    short_desc = ""
                    size_tag = soup.new_tag("p")
                    size_tag.string = str(size) if isinstance(size, str) else ""
                    variables_tag = soup.new_tag("p")
                    variables_tag.string = str(variables) if isinstance(variables, str) else ""
                    colors_tag = soup.new_tag("p")
                    colors_tag.string = str(colors) if color_list else ""
                    [desc.append(tag) for tag in [size_tag, variables_tag, colors_tag]]
                    vars = ""
                    slug = slugify(title) + "-bigser-" + str(i)
                    image_div = soup.find("div", class_="list")
                    link_list = ["http://bigser.kg" + img.get("data-zoom-image") for img in image_div.findAll("div", class_="item")]
                    links = ",".join(link_list)
                    product_fields = [title, code, short_desc, price, vars, available, links, str(slug), str(desc)]
                    endrange = 3 + len(product_fields)
                    write_products = list(
                        map(lambda r, c: products_list.write(l, c, r), product_fields, [c for c in range(3, endrange)]))
                    self.stdout.write(self.style.SUCCESS("%s записан. Товар по счету %s" % (title, i)))
                else:
                    self.stdout.write(self.style.NOTICE("Товар пропущен."))
            else:
                count += 1
                self.stdout.write(self.style.ERROR(" Нет такой страницы 404"))
            if count >= 200:
                break
        file_name = "bigser.xls"
        wb.save("dump/" + file_name)
        self.stdout.write(self.style.SUCCESS("Done!"))



