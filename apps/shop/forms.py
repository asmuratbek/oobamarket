from django.forms import ModelForm, forms
from .models import Shop, Banners


# class ShopForm(ModelForm):
#     # class Meta:
#     #     model = Shop
#     #     fields = ['title', 'logo', 'email', 'phone', 'short_description', 'description', 'user', 'slug',]


class ShopForm(ModelForm):
    class Meta:
        model = Shop
        exclude = ['user', 'slug']


class ShopBannersForm(ModelForm):
    class Meta:
        model = Banners
        fields = ['title', 'image']
