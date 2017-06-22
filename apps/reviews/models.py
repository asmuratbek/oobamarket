from django.db import models

# Create your models here.
from apps.product.models import Product
from apps.shop.models import Shop
from apps.users.models import User
from apps.utils.models import PublishBaseModel

REVIEW_STARS = (
    ('*', u'очень плохо'),
    ('**', u'плохо'),
    ('***', u'удовлетворительно'),
    ('****', u'хорошо'),
    ('*****', u'отлично'),
)


class AbstractReview(PublishBaseModel):
    class Meta:
        abstract = True

    user = models.ForeignKey(User, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Отзыв')
    stars = models.CharField(max_length=100, verbose_name='Звездочки', choices=REVIEW_STARS, null=True, blank=True)


class ProductReviews(AbstractReview):
    class Meta:
        verbose_name = "Отзыв товара"
        verbose_name_plural = "Отзывы товара"

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')

    def __str__(self):
        return str(self.product)


class ShopReviews(AbstractReview):
    class Meta:
        verbose_name = 'Отзыв магазина'
        verbose_name_plural = 'Отзывы магазинов'

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Магазин')

    def __str__(self):
        return self.shop
