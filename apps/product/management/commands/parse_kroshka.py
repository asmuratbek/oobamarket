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
        for page in range(1, max_page):
            page_html = requests.get(url.format(page=page)).content
            page_soup = BeautifulSoup(page_html, 'lxml')
            products_article = page_soup.find("article", class_="products-wrap").find_all("a", class_="blue")
            products_links = [a.get("href") for a in products_article]
            for link in products_links:
                item_html = requests.get(link).content
                item_soup = BeautifulSoup(item_html, 'lxml')
                category_links = item_soup.find("div", class_="section-bread-crumbs").find_all("a")
                categories = [a.string for a in category_links[1:]]
                item_content = item_soup.find("div", class_="product-content")
                product_content = item_content.find("div", class_="clearfix")
                title = item_content.find("h1").string
                price = item_content.find("span", class_="product-price-data").string
                available = item_content.find("span", class_="infoDigits").string
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


