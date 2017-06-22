import json, os
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile, InMemoryUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from config.settings.base import MEDIA_ROOT
from apps.users.tests.factories import UserFactory
from .factories import *
# Create your tests here

media = MEDIA_ROOT + '/'


class BannersTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()

    def test_should_add_banner_if_form_is_valid(self):
        shop = ShopFactory()
        shop.user.add(self.user)
        shop.save()
        im = Image.new(mode='RGB', size=(200, 200,))
        im_io = BytesIO()
        im.save(im_io, 'JPEG')
        im_io.seek(0)
        img = InMemoryUploadedFile(im_io, None, 'some-name.jpg', 'image/jpeg', 3204, None)
        data = {'image': img}
        self.client.login(username=self.user.username, password='password')
        response = self.client.post(reverse('shops:add_banner', kwargs={'slug': shop.slug}), data=data)
        self.assertEqual(json.loads(response.content.decode('utf-8'))['is_valid'], True)
        self.addCleanup(os.remove, media + 'images/shop/banners/some-name.jpg')

    def test_should_remove_banner(self):
        shop = ShopFactory()
        shop.user.add(self.user)
        shop.save()
        banner = BannerFactory(shop=shop)
        data = {'banner_id': banner.id, 'shop_slug': shop.slug}
        self.client.login(username=self.user.username, password='password')
        response = self.client.post(reverse('shops:delete-banners'), data=data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode('utf-8'))['status'], 0)
        self.addCleanup(os.remove, media + banner.image.name)

    def test_should_return_404_if_banner_is_empty(self):
        shop = ShopFactory()
        shop.user.add(self.user)
        shop.save()
        data = {'banner_id': 100500, 'shop_slug': shop.slug}
        self.client.login(username=self.user.username, password='password')
        response = self.client.post(reverse('shops:delete-banners'), data=data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)
