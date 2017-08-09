import urllib.request, requests, random
from requests.exceptions import ProxyError, ConnectionError
from django.core.management import BaseCommand
from bs4 import BeautifulSoup
from django.conf import settings
from django.utils.html import strip_tags
from slugify import slugify
from xlwt import Workbook


class Command(BaseCommand):
    help = "This func parse products from www.watch.kg"


    def get_user_agent(self):
        f = open(str(settings.ROOT_DIR) + "/apps/product/management/commands/user_agents.txt").read().split("\n")
        user_agent = random.choice(f)
        return user_agent

    def get_proxy(self):
        proxy_html = requests.get("https://hidemy.name/ru/proxy-list/?country=KZRU&type=h&anon=1#list",
                                  headers={'User-Agent': self.get_user_agent()}).content
        proxy_soup = BeautifulSoup(proxy_html, 'lxml')
        proxy_table = proxy_soup.find("table", class_="proxy__t").find("tbody")
        if proxy_table:
            proxy_tags = proxy_table.find_all("tr")
            proxy_list = ["http://{host}:{port}".format(host=px.find("td", class_="tdl").string,
                          port=px.find("td", class_="tdl").find_next_sibling("td").string) for px in proxy_tags]
            for proxy in proxy_list:
                try:
                    resp = requests.get("http://watch.kg/", proxies={"http": proxy})
                    if resp.status_code == 200:
                        return proxy
                except ConnectionError:
                    continue

    def handle(self, *args, **options):
        url = "http://watch.kg/page/{page}/?s&post_type=product"
        html = requests.get(url.format(page=1)).content
        soup = BeautifulSoup(html, 'lxml')
        max_pages = int(soup.find("ul", class_="page-numbers").find_all("a")[-2].string) + 1
        wb = Workbook(encoding="utf-8")
        products_list = wb.add_sheet(u"Товары", cell_overwrite_ok=True)
        l = 0
        for page in range(1, max_pages):
            proxy = {"http": self.get_proxy()}
            headers = {'User-Agent': self.get_user_agent()}
            page_html = requests.get(url.format(page=page), headers=headers, proxies=proxy)
            page_html = page_html.content
            page_soup = BeautifulSoup(page_html, 'lxml')
            products_links = [link.get("href") for link in page_soup.find("ul", class_="products")
                                .find_all("a", class_="woocommerce-LoopProduct-link")]
            for product in products_links:
                l += 1
                item_html = requests.get(product, headers=headers, proxies=proxy)
                item_html = item_html.content
                item_soup = BeautifulSoup(item_html, 'lxml')
                cats_tag = item_soup.find("nav", class_="woocommerce-breadcrumb")
                cats = [a.string for a in cats_tag.find_all("a")[2:]]
                item_content = item_soup.find("main", id="main")
                title = item_content.find("h1", class_="product_title").string
                price = item_content.find("p", class_="price").find("span", class_="woocommerce-Price-amount")
                if price:
                    price = price.string
                images_list = [img.get("src") for img in item_content.find("div", class_="images").find_all("img")]
                if len(images_list) > 1:
                    images_list = [img.get("src") for img in item_content.find("div", class_="images")
                                    .find("div", class_="thumbnails").find_all("img")]
                images = ",".join(images_list)
                short_desc = ""
                available = "Есть"
                slug = slugify(title)
                desc = item_content.find("div", id="tab-description")
                if desc:
                    clear_desc = [i.extract() for i in desc.find_all("div", class_="the_champ_sharing_container")]
                else:
                    desc = ""
                code, colors = "", ""
                product_fields = [title, code, short_desc, price, colors, available, images, str(slug), str(desc)]
                endrange = 3 + len(product_fields)
                write_cats = list(
                    map(lambda r, c: products_list.write(l, c, r), cats, [c for c in range(len(cats))]))
                write_products = list(
                    map(lambda r, c: products_list.write(l, c, r), product_fields, [c for c in range(3, endrange)]))
                self.stdout.write(self.style.SUCCESS("%s записан. По счету - %s" % (title, l)))
        file_name = "watch_products.xls"
        wb.save("dump/" + file_name)
        self.stdout.write(self.style.SUCCESS("Done!"))


