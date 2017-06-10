from django.db import models

# Create your models here.
from django.urls import reverse
from apps.utils.models import PublishBaseModel


class GlobalCategory(PublishBaseModel):

    class Meta:
        verbose_name = 'Глобальная категория'
        verbose_name_plural = 'Глобальные категории'

    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.CharField(max_length=255, verbose_name='Название на транслите')
    icon = models.ImageField(upload_to="category/icons", default=None)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("categories:global_detail", kwargs={'slug': self.slug})

    def get_icon(self):
        return self.icon.url if self.icon else None

    def get_products(self):
        from apps.product.models import Product
        categories = self.category_set.all()
        product_ids = list()
        for category in categories:
            product_ids += [product.id for product in category.get_products()]
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_parent_categories(self):
        return self.category_set.filter(parent=None)
