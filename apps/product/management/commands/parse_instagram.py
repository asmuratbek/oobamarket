import urllib.request, requests, json, uuid
from django.core.management import BaseCommand
from django.conf import settings
from apps.shop.models import Shop
from slugify import slugify
from apps.category.models import Category
from apps.product.models import Product, ProductImage


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('username', nargs="+", type=str)
        parser.add_argument('slug', nargs="+", type=str)

    def get_user_id(self, username):
        url = "https://api.instagram.com/v1/users/search?q={username}&access_token={token}"
        response = requests.get(url.format(username=username, token=settings.INSTAGRAM_ACCESS_TOKEN))
        data = json.loads(response.content.decode("utf-8"))['data']
        if data:
            user_id = data[0]['id']
            return user_id
        return self.stdout.write(self.style.ERROR("Пользователь '{}' не найден.".format(username)))

    def handle(self, *args, **options):
        username = options['username'][0]
        shop_slug = options['slug'][0]
        user_id = self.get_user_id(username)
        category = Category.objects.filter(title__icontains="Разное").first()
        try:
            shop = Shop.objects.get(slug=shop_slug)
        except Shop.DoesNotExist:
            return self.stdout.write(self.style.ERROR("Магазин '{}' не найден."))
        url = "https://api.instagram.com/v1/users/{id}/media/recent/?access_token={token}"
        response = requests.get(url.format(id=user_id, token=settings.INSTAGRAM_ACCESS_TOKEN))
        data = json.loads(response.content.decode("utf-8"))
        meta = data['meta']
        if meta['code'] == 200:
            content = data['data']
            download = urllib.request.urlretrieve
            for product in content:
                img_id = product['id']
                img_list = list()
                try:
                    links = [link['images']['standard_resolution']['url']
                             for link in product['carousel_media'] if link['type'] == 'image']
                    download_img = [download(img, settings.MEDIA_ROOT + "/products/image/" + img.split("/")[-1])
                                    for img in links]
                    [img_list.append(str(i.split("/")[-1])) for i in links]
                except KeyError:
                    download_img = download(product['images']['standard_resolution']['url'],
                                            settings.MEDIA_ROOT + "/products/image/" + img_id + ".jpg")
                    img_list.append(str(img_id + ".jpg"))
                if product['caption']:
                    title = product["caption"]["text"]
                    if "." in title:
                        title = title.split(".")[0]
                    desc = product['caption']['text']
                else:
                    title = "Не указано"
                    desc = ""
                slug = str(slugify(title)) + "-" + str(uuid.uuid4())
                prod = Product.objects.create(title=title, slug=slug, category=category, shop=shop,
                                              short_description=desc)
                prod_images = [ProductImage.objects.create(product=prod, image="products/image/" + image)
                               for image in img_list]
                self.stdout.write(self.style.SUCCESS("{} создан.".format(title)))
            return self.stdout.write(self.style.SUCCESS("Done!"))
        else:
            return self.stdout.write(self.style.ERROR("Недостаточно прав для просмотра данного юзера."))

