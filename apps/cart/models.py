from decimal import Decimal
from django.db import models

# Create your models here.
from django.db.models.signals import pre_save, post_save, post_delete

from apps.product.models import Product
from apps.shop.models import Shop
from apps.users.models import User
from django.utils.translation import ugettext as _
from apps.utils.models import PublishBaseModel


class Cart(PublishBaseModel):

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    user = models.ForeignKey(User, null=True, blank=True, verbose_name="Владелец")
    subtotal = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    def get_delivery_total(self):
        delivery_total = 0
        for index, shop in enumerate(range(self.get_shops().count())):
            if index == 0:
                delivery_total += 150
            else:
                delivery_total += 100
        return delivery_total


    def update_subtotal(self):
        subtotal = 0
        items = self.cartitem_set.all()
        for item in items:
            subtotal += item.total
        subtotal += self.get_delivery_total()
        self.subtotal = "%.2f" % (subtotal)
        self.save()

    def subtotal_for_shop(self, shop):
        subtotal = 0

        for item in self.cartitem_set.filter(product__shop=shop):
            subtotal += item.total

        # subtotal += self.get_delivery_total()
        return "%.2f" % (subtotal)

    def get_shops(self):
        products = self.cartitem_set.all()
        product_ids = [product.product.id for product in products]
        shops = Shop.objects.filter(product__id__in=product_ids).distinct()
        return shops

    def empty(self):
        for item in self.cartitem_set.all():
            item.delete()

    def get_cart_items_count(self):
        return self.cartitem_set.count()


class CartItem(models.Model):

    class Meta:
        verbose_name = "Продукт в корзине"
        verbose_name_plural = "Продукты в корзине"

    cart = models.ForeignKey(Cart, verbose_name='Корзина')
    product = models.ForeignKey(Product, verbose_name='Продукт', null=True, blank=True)
    quantity = models.PositiveIntegerField(_("Количество"), default=1)
    comments = models.TextField(_("Комментарии к продукту"), null=True, blank=True)
    total = models.DecimalField(_("Общая цена"), max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product.title

    def get_shops(self):
        products = self.product.all()
        product_ids = [product.product.id for product in products]
        shops = Shop.objects.filter(product__id__in=product_ids).distinct()
        return shops

def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
    qty = instance.quantity
    if int(qty) >= 1:
        price = instance.product.get_price()
        total = Decimal(qty) * Decimal(price)
        instance.total = "%.2f" % (total)

pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)


def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
    instance.cart.update_subtotal()

post_save.connect(cart_item_post_save_receiver, sender=CartItem)

post_delete.connect(cart_item_post_save_receiver, sender=CartItem)
