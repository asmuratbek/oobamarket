from django.test import TestCase, Client
from django.urls import reverse

from .factories import ProductFactory, ProductImageFactory
from apps.users.tests.factories import UserFactory
from apps.shop.factories import ShopFactory
from apps.category.factories import CategoryFactory
from apps.global_category.factories import GlobalCategoryFactory
from apps.properties.factories import PropetiesFactory, ValueFactory
# Create your tests here.


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

