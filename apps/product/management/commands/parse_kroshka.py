import urllib.request, requests
from django.core.management import BaseCommand
from bs4 import BeautifulSoup
from slugify import slugify
from xlwt import Workbook


class Command(BaseCommand):
    help = "Parse products from www.kroshka-bishkek.ru"

    def handle(self, *args, **options):
        url = "http://kroshka-bishkek.ru/products/search?sort=0&balance=&categoryId=&min_cost=&max_cost=&page={page}"
        html = requests.get(url.format(page=1)).content
        soup = BeautifulSoup(html, 'lxml')
        pagination_links = soup.find("ul", class_="pagination").find_all("a")
        max_page = int(pagination_links[-1].string) + 1
        wb = Workbook(encoding="utf-8")
        products_list = wb.add_sheet(u"Товары", cell_overwrite_ok=True)
        for page in range(1, max_page):
            page_html = requests.get(url.format(page=page)).content
            page_soup = BeautifulSoup(page_html, 'lxml')
            products_article = page_soup.find("article", class_="products-wrap").find_all("a", class_="blue")
            products_links = [a.get("href") for a in products_article]
            l = 0
            for link in products_links:
                l += 1
                item_html = requests.get(link).content
                item_soup = BeautifulSoup(item_html, 'lxml')
                category_links = item_soup.find("div", class_="section-bread-crumbs").find_all("a")
                categories = [a.string for a in category_links[1:]]
                item_content = item_soup.find("div", class_="product-content")
                product_content = item_content.find("div", class_="clearfix")
                title = item_content.find("h1").string
                price = item_content.find("span", class_="product-price-data").string
                available = item_content.find("span", class_="infoDigits smallChars").string
                if available.startswith("в наличии"):
                    if int(available.split(":")[-1]) > 0:
                        available = "Есть"
                    else:
                        available = "Нет"
                else:
                    available = "Нет"
                short_desc = product_content.find("div", class_="user-inner")
                avatar = item_content.find("div", class_="avatar-view").find("img").get("src")
                avatar_link = "http:" + avatar
                img_list = [avatar_link]
                prod_photos = item_content.find("div", class_="product-photos")
                if prod_photos:
                    img_links = ["http:" + img.get("src") for img in prod_photos.find_all("img")]
                    img_list += img_links
                desc_div = item_content.find_all("div", class_="user-inner")
                desc = desc_div[-1] if len(desc_div) > 1 else None
                desc_images = desc.find_all("img") if desc else []
                images = ["http:" + img.get("src") for img in desc_images]
                new_image_tags = [item_soup.new_tag("img", src=c) for c in images]
                write_images = list(map(lambda r,c: r.replace_with(c), desc_images, new_image_tags))
                slug = link.split("/")[-1]
                code, colors = "", ""
                photos = ",".join(img_list)
                product_fields = [title, code, short_desc, price, colors, available, photos, str(slug), str(desc)]
                endrange = 3 + len(product_fields)
                write_cats = list(
                    map(lambda r, c: products_list.write(l, c, r), categories, [c for c in range(len(categories))]))
                write_products = list(
                    map(lambda r, c: products_list.write(l, c, r), product_fields, [c for c in range(3, endrange)]))
                self.stdout.write(self.style.SUCCESS("%s записан." % title))
        file_name = "kroshka_products.xls"
        wb.save("dump/" + file_name)
        self.stdout.write(self.style.SUCCESS("Done!"))

# Some changes
# Some new changes
