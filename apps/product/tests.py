import json, tempfile, mock
import os

from PIL import Image
from io import BytesIO

from apps.product.forms import ProductImagesForm
from config.settings.base import MEDIA_ROOT
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile, InMemoryUploadedFile
from django.core.files import File
from config.settings.base import MEDIA_ROOT
from .factories import ProductFactory, ProductImageFactory, FavoriteProductFactory
from apps.users.tests.factories import UserFactory
from apps.shop.factories import ShopFactory
from apps.category.factories import CategoryFactory
from apps.global_category.factories import GlobalCategoryFactory
from apps.properties.factories import PropetiesFactory, ValueFactory
from django.test import override_settings
# Create your tests here.


media = MEDIA_ROOT + '/'


def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, 'jpeg')
    return temp_file


class ProductCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        # self.product = ProductFactory(price=150)
        self.user = UserFactory()

    def test_should_create_product_if_form_is_valid(self):
        shop = ShopFactory()
        shop.user.add(self.user)
        shop.save()
        global_category = GlobalCategoryFactory()
        category = CategoryFactory(section=global_category)
        images = [ProductImageFactory() for i in range(2)]
        self.client.login(username=self.user.username, password='password')
        data = {'shop': shop.id, 'long_description': '',
                'discount': '', 'delivery_cost': '',
                'quantity': 1, 'title': 'Some product',
                'delivery_type': 'self', 'removed_images': '%s' % images[1].id,
                'price': '555', 'property-1': '------------', 'property-2': '------------','published': 'on',
                'category': category.id, 'currency': 'сом', 'availability': 'available',
                'uploaded_images': '%s, %s' % (images[0].id, images[1].id), 'short_description': ''}
        response = self.client.post(reverse('product:add_product', kwargs={'slug': shop.slug}), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(shop.product_set.last().title, 'Some product')
        self.assertEqual(shop.product_set.last().productimage_set.count(), 1)
        self.assertEqual(shop.product_set.last().productimage_set.first().id, images[0].id)
        self.addCleanup(os.remove, media + images[0].image.name)


class ProductUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()

    def test_should_update_product_if_form_is_valid(self):
        shop = ShopFactory()
        shop.user.add(self.user)
        shop.save()
        global_category = GlobalCategoryFactory()
        parent_category = CategoryFactory(section=global_category)
        sub_category = CategoryFactory(parent=parent_category)
        product = ProductFactory(title="Product for test",
                                 price=1500, shop=shop,
                                 category=sub_category, quantity=4)
        images = [ProductImageFactory(product=product) for i in range(2)]
        properties = [PropetiesFactory(order=1+i) for i in range(2)]
        properties[0].category.add(sub_category), properties[1].category.add(sub_category)
        values = [ValueFactory(properties=p, order=1+properties.index(p)) for p in properties]
        values[0].products.add(product), values[1].products.add(product)
        new_parent_category = CategoryFactory(section=global_category)
        new_sub_category = CategoryFactory(parent=new_parent_category)
        new_shop = ShopFactory()
        new_shop.user.add(self.user)
        new_shop.save()
        self.client.login(username=self.user.username, password='password')
        data = {'currency': 'рублей', 'property-%s' % values[1].properties.id: values[1].id, 'section': global_category.id,
                'title': 'Some phone23', 'delivery_type': 'self', 'quantity': '2',
                'short_description': 'Some desc', 'shop': new_shop.id, 'parent_categories':new_parent_category.id,
                'image': '', 'property-%s' % values[0].properties.id: values[0].id, 'category': new_sub_category.id, 'price': 1000,
                'published': 'off', 'availability': 'waiting', 'long_description': ''}
        response = self.client.post(reverse('product:update_product', kwargs={'slug': product.slug}), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(new_sub_category.product_set.last().price, 1000)
        self.assertEqual(new_sub_category.product_set.last().shop, new_shop)
        self.assertEqual(new_sub_category.product_set.last().values_set.last().id, values[1].id)
        self.addCleanup(os.remove, media + images[0].image.name)
        self.addCleanup(os.remove, media + images[1].image.name)


class FavoriteProductTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()

    def test_should_create_favorite_product_if_valid(self):
        data = {'item': 1}
        self.client.login(username=self.user.username, password='password')
        response = self.client.get(reverse('create_favorite'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode('utf-8'))['flash_message'], 'Продукт успешно добавлен в избранное')

    def test_should_remove_favorite_product_if_valid(self):
        self.client.login(username=self.user.username, password='password')
        product = ProductFactory(price=1550)
        favorite = FavoriteProductFactory(product=product, user=self.user)
        data = {'item': favorite.id}
        response = self.client.get(reverse('create_favorite'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode('utf-8'))['flash_message'], 'Продукт успешно удален из избранных')


class ProductImagesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()

    def test_should_upload_image_if_valid(self):
        file_mock = mock.MagicMock(spec=File, name='FileMock')
        data = {'file-0': file_mock}
        response = self.client.post(reverse('product:upload_images'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content.decode('utf-8'))['uploaded_files'])
        self.addCleanup(os.remove, media + 'products/image/file-0')

    def test_should_upload_multiple_images_if_valid(self):
        # file_mock = mock.MagicMock(spec=File, name='FileMock')
        # data = {'file-{}'.format(i): file_mock for i in range(3)}
        up_img = SimpleUploadedFile
        multiple_img = [up_img('default-%s.jpg' % i, b"file_content", content_type='image/jpeg') for i in range(3)]
        data = {'file-{}'.format(multiple_img.index(img)): img for img in multiple_img}
        response = self.client.post(reverse('product:upload_images'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content.decode('utf-8'))['uploaded_files']), 3)
        self.addCleanup(os.remove, media + 'products/image/default-0.jpg')
        self.addCleanup(os.remove, media + 'products/image/default-1.jpg')
        self.addCleanup(os.remove, media + 'products/image/default-2.jpg')

    def test_should_remove_images(self):
        product = ProductFactory(price=1500)
        product_images = [ProductImageFactory(product=product) for i in range(3)]
        ids = [img.id for img in product_images]
        data = {'media_ids': ids}
        response = self.client.post(reverse('product:remove_images'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode('utf-8'))['done'], True)
        self.addCleanup(os.remove, media + product_images[0].image.name)
        self.addCleanup(os.remove, media + product_images[1].image.name)

    def test_should_return_false_if_called_empty_body(self):
        data = {'media_ids': ''}
        response = self.client.post(reverse('product:remove_images'), data=data)
        self.assertEqual(json.loads(response.content.decode('utf-8'))['done'], False)


class ProductDeleteView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()

    def test_should_delete_product(self):
        product = ProductFactory(price=1500)
        response = self.client.post(reverse('product:delete_product', kwargs={'slug': product.slug}))
        self.assertEqual(response.status_code, 302)


class ChangePublishStatus(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()

    def test_should_change_status_on_published_false(self):
        product = ProductFactory(price=1500, published=True)
        response = self.client.get(reverse('product:change_publish_status'), data={'item': product.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode('utf-8'))['message'], 'Продукт успешно скрыт')

    def test_should_change_status_on_published_true(self):
        product = ProductFactory(price=1500, published=False)
        response = self.client.get(reverse('product:change_publish_status'), data={'item': product.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode('utf-8'))['message'], 'Продукт успешно опубликован')

    def test_should_return_404_if_product_does_not_exist(self):
        response = self.client.get(reverse('product:change_publish_status'), data={'item': 100500})
        self.assertEqual(response.status_code, 404)


class ProductImagesUpdateTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()

    def test_should_upload_image(self):
        im = Image.new(mode='RGB', size=(200, 200,))
        im_io = BytesIO()
        im.save(im_io, 'JPEG')
        im_io.seek(0)
        image = InMemoryUploadedFile(im_io, None, 'some-name.jpg', 'image/jpeg', 3204, None)
        img = dict(image=image)
        product = ProductFactory(price=1500)
        self.client.login(username=self.user.username, password='password')
        response = self.client.post(reverse('product:upload_product_images', kwargs={'slug': product.slug}), data=img,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode('utf-8'))['is_valid'], True)
        self.addCleanup(os.remove, media + 'products/image/some-name.jpg')

    def test_should_delete_product_image(self):
        product = ProductFactory(price=1500)
        product_image = ProductImageFactory(product=product)
        data = dict(productimage_id=product_image.id)
        self.client.login(username=self.user.username, password='password')
        response = self.client.post(reverse('product:delete_product_images'), data=data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode('utf-8'))['status'], 0)

    def test_should_return_error_if_product_image_field_is_empty(self):
        data = dict(productimage_id='')
        self.client.login(username=self.user.username, password='password')
        response = self.client.post(reverse('product:delete_product_images'), data=data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content.decode('utf-8'))['status'], 1)
