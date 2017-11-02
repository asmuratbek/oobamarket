import imghdr, os, xlwt
import urllib.request
from openpyxl import Workbook as new_wb, load_workbook

from django.core.mail import EmailMessage
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
from datetime import datetime

from apps.users.models import User


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


def send_letters_to_shop(cart):
    shops = cart.get_shops()
    order = cart.simpleorder_set.first()
    name, phone, address, date = order.name, order.phone, order.address, datetime.now()
    message = u"Поступил новый заказ: \n " + u"Имя: %s \n " % name + u"Номер телефона: %s \n " % phone \
              + "Адрес: %s \n " % address + "Дата: %s \n " % date
    style_string = "font: bold on"
    style = xlwt.easyxf(style_string)
    shop_files = list()
    for shop in shops:
        wb = Workbook(encoding='utf-8')
        products_list = wb.add_sheet(u"Магазин - {}".format(shop.title), cell_overwrite_ok=True)
        cartitems = cart.cartitem_set.filter(product__shop=shop)
        titles = [u"Наименование товара", u"Количество", u"Цена", u"Комментарии", u"Сумма"]
        end_rows = [u"Итого", u"Доставка"]
        end_rows_values = [sum(cartitems.values_list('total', flat=True)), 150]
        products_names = [item.product.title for item in cartitems]
        products_qty = [item.quantity for item in cartitems]
        products_price = [item.product.price for item in cartitems]
        products_comments = [item.comments for item in cartitems]
        products_total = [item.total for item in cartitems]
        max_rows_num_items = cartitems.count() + 1
        write_titles = list(map(lambda i, c: products_list.write(0, c, i, style=style), titles, [c for c in range(len(titles))]))
        write_products_name = list(map(lambda i, c: products_list.write(c, 0, i), products_names, [c for c in range(1, len(products_names) + 1)]))
        write_products_qty = list(map(lambda i, c: products_list.write(c, 1, i), products_qty, [c for c in range(1, len(products_qty) + 1)]))
        write_products_price = list(map(lambda i, c: products_list.write(c, 2, i), products_price, [c for c in range(1, len(products_price) + 1)]))
        write_products_comments = list(map(lambda i, c: products_list.write(c, 3, i), products_comments, [c for c in range(1, len(products_comments) + 1)]))
        write_products_total = list(map(lambda i, c: products_list.write(c, 4, i), products_total, [c for c in range(1, len(products_total) + 1)]))
        write_end_rows = list(map(lambda i, c: products_list.write(c, 0, i, style=style), end_rows, [c for c in range(max_rows_num_items, max_rows_num_items + len(end_rows) + 1)]))
        write_end_rows_vals = list(map(lambda i, c: products_list.write(c, 4, i), end_rows_values, [c for c in range(max_rows_num_items, max_rows_num_items + len(end_rows) + 1)]))
        file_name = "order-{}-{}.xls".format(cart.id, shop.slug)
        shop_files.append(file_name)
        wb.save(file_name)
        email_message = EmailMessage("{} - {}".format(name, phone), message, settings.EMAIL_HOST_USER, [user.email for user in shop.user.all()])
        email_message.attach_file(file_name)
        email_message.send()
    email_message = EmailMessage("{} - {}".format(name, phone), message, settings.EMAIL_HOST_USER,
                                 [user.email for user in User.objects.filter(is_staff=True)])
    [email_message.attach_file(file_name) for file_name in shop_files]
    email_message.send()
    try:
        [os.remove(f) for f in shop_files]
    except FileNotFoundError:
        print("file not found")
    print("ok")




