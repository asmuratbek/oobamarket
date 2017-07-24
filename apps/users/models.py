from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

SUBSCRIPTION_TYPES = (
    ("all", "Все"),
    ("only_actions", "Акции"),
    ("only_products", "Товары"),
)


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    phone = models.CharField(_('Phone number'), null=True, blank=True, max_length=255)

    def __str__(self):
        return self.username

    def get_username(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def get_favorites_count(self):
        return self.favoriteproduct_set.count()

    def get_favorites(self):
        return self.favoriteproduct_set.all()

    def get_favorites_link(self):
        return reverse("users:favorites", kwargs={'pk': self.pk})

    def get_original_products(self):
        from apps.product.models import Product
        product_ids = list()
        for product in self.favoriteproduct_set.all():
            product_ids.append(product.product.id)
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_cart_count(self):
        if self.cart_set.exists():
            return self.cart_set.last().cartitem_set.count()
        else:
            return 0

    def shops_name(self):
        return self.shop_set.all()


class Subscription(models.Model):
    user = models.ForeignKey(User)
    subscription = models.ForeignKey('shop.Shop', verbose_name='Подписка на магазины', related_name='sub_shops')
    subscription_type = models.CharField(max_length=50, choices=SUBSCRIPTION_TYPES, verbose_name='Тип подписки', default='all')
