from django.db import models

# Create your models here.
from apps.product.models import Product
from apps.users.models import User
from django.utils.translation import ugettext as _


class Cart(models.Model):

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    user = models.OneToOneField(User, null=True, blank=True, verbose_name="Владелец")
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    subtotal = models.DecimalField(max_digits=50, decimal_places=2, default=25.00)
    total = models.DecimalField(max_digits=50, decimal_places=2, default=25.00)

    def __str__(self):
        return str(self.id)

    def update_subtotal(self):
        subtotal = 0
        items = self.cartitem_set.all()
        for item in items:
            subtotal += item.total
        self.subtotal = "%.2f" % (subtotal)
        self.save()


class CartItem(models.Model):

    class Meta:
        verbose_name = "Продукт в корзине"
        verbose_name_plural = "Продукты в корзине"

    cart = models.ForeignKey(Cart, verbose_name='Корзина')
    product = models.ForeignKey(Product, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(_("Количество"), default=1)
    total = models.DecimalField(_("Общая цена"), max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product.title
