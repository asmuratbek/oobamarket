import json, os, random, string
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from config.settings.base import MEDIA_ROOT
from apps.users.tests.factories import UserFactory
from .factories import *
from config.settings.base import DEFAULT_IMAGE
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


class SocialLinksView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()

    def test_should_update_socialinks_if_all_form_is_valid(self):
        shop = ShopFactory()
        shop.user.add(self.user)
        shop.save()
        data = {'twitter': 'twitter',
                'facebook': 'facebook',
                'vk': 'vkontakte',
                'instagram': 'instagram'}
        self.client.login(username=self.user.username, password='password')
        response = self.client.post(reverse('shops:update_social', kwargs={'slug': shop.slug}), data=data)
        self.assertEqual(response.status_code, 302)

    def test_should_return_new_social_obj_if_shop_hasnt_social(self):
        shop = ShopFactory(sociallinks=None)
        shop.user.add(self.user)
        shop.save()
        self.client.login(username=self.user.username, password='password')
        response = self.client.get(reverse('shops:update_social', kwargs={'slug': shop.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(shop.sociallinks.shop)


class ShopCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()

    def test_should_create_shop_if_all_values_is_valid(self):
        generate_str = ''.join([random.choice(string.ascii_lowercase) for i in range(10)])
        places = [PlaceFactory(title=generate_str, type='mall') for i in range(2)]
        im = Image.new(mode='RGB', size=(200, 200,))
        im_io = BytesIO()
        im.save(im_io, 'JPEG')
        im_io.seek(0)
        img = InMemoryUploadedFile(im_io, None, 'some-logo.jpg', 'image/jpeg', 3204, None)
        data = {'contacts_set-MAX_NUM_FORMS': '1000', 'email': self.user.email,
                'contacts_set-2-shop': '', 'contacts_set-2-phone': '0707170017',
                'contacts_set-2-id': '', 'contacts_set-TOTAL_FORMS': '3', 'contacts_set-0-shop': '',
                'place': [places[0].id, places[1].id], 'contacts_set-1-shop': '',
                'description': 'Купи слона',
                'contacts_set-2-address': 'Some value 2', 'contacts_set-MIN_NUM_FORMS': '0',
                'contacts_set-0-phone': 'address', 'contacts_set-0-address': 'Some value 0',
                'contacts_set-1-id': '', 'contacts_set-0-id': '',
                'contacts_set-2-published': 'on', 'contacts_set-1-phone': 'Some value 1',
                'contacts_set-0-published': 'on', 'contacts_set-1-published': 'on',
                'contacts_set-INITIAL_FORMS': '0', 'title': 'Купи слона',
                'short_description': 'Some short description',
                'contacts_set-1-address': 'address', 'logo': img}
        self.client.login(username=self.user.username, password='password')
        response = self.client.post(reverse('shops:create'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user.shop_set.last().logo)
        self.assertEqual(self.user.shop_set.last().email, self.user.email)
        self.assertEqual(self.user.shop_set.last().contacts_set.count(), 3)
        self.addCleanup(os.remove, media + 'images/shop/logo/some-logo.jpg')


class ShopUdateViewTest(TestCase):
    def setUp(self):
        self.client  = Client()
        self.user = UserFactory()

    def test_should_update_shop_if_all_values_is_valid(self):
        shop = ShopFactory()
        generate_str = ''.join([random.choice(string.ascii_lowercase) for i in range(10)])
        contacts = [ContactsFactory(address='phone', phone='value-%s' % i, shop=shop) for i in range(3)]
        im = Image.new(mode='RGB', size=(200, 200,))
        im_io = BytesIO()
        im.save(im_io, 'JPEG')
        im_io.seek(0)
        img = InMemoryUploadedFile(im_io, None, 'some-logo.jpg', 'image/jpeg', 3204, None)
        shop.logo = img
        shop.user.add(self.user)
        shop.save()
        data = {'contacts_set-MAX_NUM_FORMS': '1000', 'email': 'some_new_email@email.com',
                'contacts_set-2-shop': shop.id, 'contacts_set-2-address': 'phone',
                'contacts_set-2-id': contacts[2].id, 'contacts_set-TOTAL_FORMS': '3', 'contacts_set-0-shop': shop.id,
                'contacts_set-1-shop': shop.id,
                'description': 'Some new description',
                'contacts_set-2-phone': 'Some new_value 2', 'contacts_set-MIN_NUM_FORMS': '0',
                'contacts_set-0-address': 'address', 'contacts_set-0-phone': 'Some new_value 0',
                'phone': '9965596677492', 'contacts_set-1-id': contacts[1].id, 'contacts_set-0-id': contacts[0].id,
                'contacts_set-2-published': 'off', 'contacts_set-1-phone': 'Some new_value 1',
                'contacts_set-0-published': 'on', 'contacts_set-1-published': 'on',
                'contacts_set-INITIAL_FORMS': '0', 'title': 'Купи слона',
                'short_description': 'Some short description',
                'contacts_set-1-address': 'address', 'logo': ''}
        self.client.login(username=self.user.username, password='password')
        response = self.client.post(reverse('shops:update', kwargs={'slug': shop.slug}), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.shop_set.last().email, 'some_new_email@email.com')
        self.addCleanup(os.remove, media + 'images/shop/logo/some-logo.jpg')

    def test_should_remove_logo(self):
        im = Image.new(mode='RGB', size=(200, 200,))
        im_io = BytesIO()
        im.save(im_io, 'JPEG')
        im_io.seek(0)
        img = InMemoryUploadedFile(im_io, None, 'some-logo.jpg', 'image/jpeg', 3204, None)
        shop = ShopFactory(logo=img)
        shop.user.add(self.user)
        shop.save()
        self.client.login(username=self.user.username, password='password')
        response = self.client.post(reverse('shops:remove_logo'), data={'slug': shop.slug},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.shop_set.last().logo.name, '/default.jpg')
        self.addCleanup(os.remove, media + 'images/shop/logo/some-logo.jpg')

    def test_should_return_404_if_shop_does_not_exist(self):
        self.client.login(username=self.user.username, password='password')
        response = self.client.post(reverse('shops:remove_logo'), data={'slug': 'slug-slug'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)
