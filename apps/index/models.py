from django.db import models
from apps.utils.models import PublishBaseModel
# Create your models here.

COLUMNS_TYPES = (
    ("first_col", "Первая колонка"),
    ("second_col", "Вторая колонка"),
    ("third_col", "Третья колонка")
)

BLOCK_TYPES = (
    ("big_up_block", "Большой верхний блок"),
    ("big_down_block", "Большой нижний блок"),
    ("up_left_corner_1", "Верхняя левая сторона верхний блок"),
    ("up_left_corner_2", "Верхняя левая сторона нижний блок"),
    ("up_right_corner_1", "Верхняя правая сторона верхний блок"),
    ("up_right_corner_2", "Верхняя правая сторона нижний блок"),
    ("down_right_corner_1", "Нижняя правая сторона верхний блок"),
    ("down_right_corner_2", "Нижняя правая сторона нижний блок"),
)

BANNERS_TYPES = (
    ("offer", "Рекламное предложение"),
    ("slider", "Банер на слайдер"),
)


class IndexBlocks(PublishBaseModel):
    title = models.CharField(max_length=400, verbose_name="Название блока", null=True, blank=True)
    url = models.CharField(max_length=450, verbose_name="Урл")
    image = models.ImageField(upload_to="images/index/")
    column = models.CharField(max_length=50, verbose_name="Колонка", choices=COLUMNS_TYPES)
    row = models.PositiveSmallIntegerField(verbose_name="Ряд")

    class Meta:
        verbose_name = "Блок на главной странице"
        verbose_name_plural = "Блоки на главной странице"

    def __str__(self):
        return "{col} - {row} ряд.".format(col=self.get_column_display(), row=self.row)


class PremiumIndexBlocks(PublishBaseModel):
    title = models.CharField(max_length=300, verbose_name='Наименование блока', null=True, blank=True)
    url = models.CharField(max_length=450, verbose_name='Ссылка')
    block_type = models.CharField(max_length=100, verbose_name='Тип блока', choices=BLOCK_TYPES, unique=True)
    image = models.ImageField(upload_to='images/index/premium/', verbose_name="Изображение блока")

    class Meta:
        verbose_name = "Премиум блок"
        verbose_name_plural = "Премиум блоки на главной странице"

    def __str__(self):
        return self.get_block_type_display()


class IndexBanner(PublishBaseModel):
    image = models.ImageField(upload_to='images/index/banners/', verbose_name='Изображение банера')
    banner_type = models.CharField(max_length=50, verbose_name='Тип банера', choices=BANNERS_TYPES)
    url = models.CharField(max_length=450, verbose_name='Ссылка')

    class Meta:
        verbose_name = 'Банер'
        verbose_name_plural = 'Банера на главной странице'

    def __str__(self):
        return self.get_banner_type_display()
