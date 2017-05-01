from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)

    def __str__(self):
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
        return self.cart.cartitem_set.count()
