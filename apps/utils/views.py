import imghdr, os
import urllib.request

import requests, xlrd
from bs4 import BeautifulSoup
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from xlwt import Workbook

from apps.product.models import Product, ProductImage
from apps.shop.models import Shop
from django.conf import settings


@csrf_exempt
def counter(request):
    if request.method == 'POST' and request.is_ajax:
        slug = request.POST.get('slug', '')
        try:
            item = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            item = get_object_or_404(Shop, slug=slug)
        item.counter += 1
        item.save()
        return HttpResponse('Success')
    return HttpResponse('Error')


def change_format():
    images = ProductImage.objects.all()
    for image in images:
        try:
            valid_format = imghdr.what(image.image.path)
        except FileNotFoundError:
            continue
        if valid_format:
            if not image.image.name.endswith(valid_format):
                new_name = str(image.image.name).replace(".jpg", "." + valid_format)
                os.rename(image.image.path, settings.MEDIA_ROOT + "/" + new_name)
                image.image.name = new_name
                image.save()
                print("{} изменен".format(new_name))
    print("Done")


def create_thumbnails():
    products = Product.objects.all()
    for product in products:
        avatar_image = product.productimage_set.filter(is_avatar=True).first()
        first_image = product.productimage_set.first()
        if product.productimage_set.all():
            if avatar_image:
                try:
                    avatar_image.save()
                except Exception:
                    continue
                name = os.path.split(avatar_image.thumb_image.name)[-1]
            else:
                try:
                    first_image.create_thumbnail()
                    first_image.save()
                except Exception:
                    continue
                name = os.path.split(first_image.thumb_image.name)[-1]
            print("Миниатюра для {} создана.".format(name))
    print("Done!")


def download():
    url = "http://kroshka-bishkek.ru/products/search?sort=0&balance=&categoryId=&min_cost=&max_cost=&page={page}"
    html = requests.get(url.format(page=1)).content
    soup = BeautifulSoup(html, 'lxml')
    pagination_links = soup.find("ul", class_="pagination").find_all("a")
    max_page = int(pagination_links[-1].string) + 1
    direct = os.listdir(settings.MEDIA_ROOT + "/img2/")
    for page in range(1, max_page):
        page_html = requests.get(url.format(page=page)).content
        page_soup = BeautifulSoup(page_html, 'lxml')
        products_article = page_soup.find("article", class_="products-wrap").find_all("a", class_="blue")
        products_links = [a.get("href") for a in products_article]
        for i, link in enumerate(products_links):
            item_html = requests.get(link).content
            item_soup = BeautifulSoup(item_html, 'lxml')
            item_content = item_soup.find("div", class_="product-content")
            product_content = item_content.find("div", class_="clearfix")
            avatar = item_content.find("div", class_="avatar-view")
            img_list = list()
            if avatar:
                avatar = avatar.find("img").get("src")
                avatar_link = "http:" + avatar
                img_list.append(avatar_link)
            prod_photos = item_content.find("div", class_="product-photos")
            if prod_photos:
                img_links = ["http:" + img.get("href") for img in prod_photos.findAll("a", class_="service-album")]
                img_list += img_links
            slug = link.split("/")[-1]
            img_i = 0
            for img in img_list:
                img_format = img[-4:].replace(".", "")
                img_i += 1
                file_name = str(slug) + "-{}.{}".format(img_i, img_format)
                if file_name not in direct:
                    try:
                        download_imgs = urllib.request.urlretrieve(img, settings.MEDIA_ROOT + "/img2/" + file_name)
                        print("%s скачан. № %s" % (slug, i))
                    except Exception:
                        print("Возникла ошибка.")
                        continue
                else:
                    print("Файл уже есть.")
    print("Done!")


def change_frt():
    path_list = os.listdir(settings.MEDIA_ROOT + "/img2/")
    path_file = settings.MEDIA_ROOT + "/img2/{file_name}"
    for f in path_list:
        try:
            valid_format = imghdr.what(path_file.format(file_name=f))
        except FileNotFoundError:
            continue
        if valid_format:
            if not f.endswith(valid_format):
                now_format = f[-4:].replace(".", "")
                new_name = f.replace("." + now_format, "." + valid_format)
                os.rename(path_file.format(file_name=f), settings.MEDIA_ROOT + "/img2/" + new_name)
                print("%s изменен." % f)
    print("Done!")


def download_images_from_optovik():
    wb = xlrd.open_workbook(settings.DUMP_ROOT + "/optovik.xls")
    sheet = wb.sheet_by_index(0)
    data = [[sheet.cell_value(r, c) for c in range(3, sheet.ncols)] for r in range(sheet.nrows) if \
            sheet.row(r)[3].value != ""]
    for product in data:
        title = product[0]
        slug = product[7].lower()
        imgs_list = product[6].split(",")
        img_i = 0
        for img in imgs_list:
            img_format = img.split("?")[0][-4:].replace(".", "")
            img_i += 1
            try:
                download_imgs = urllib.request.urlretrieve(img, settings.MEDIA_ROOT + "/optovik_images/" +
                                                           str(slug) + "-{}.{}".format(img_i, img_format))
            except urllib.request.URLError:
                continue
        print("Картинки {} скачаны.".format(title))





