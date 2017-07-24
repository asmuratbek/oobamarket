from django import forms
from haystack.forms import SearchForm

from apps.category.models import Category
from apps.global_category.models import GlobalCategory
from apps.shop.models import Shop
from .models import Product, ProductImage


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['slug', 'objects', 'sell_count', 'counter']

    removed_images = forms.CharField(required=False)
    uploaded_images = forms.CharField(required=False)


    def __init__(self, *args, **kwargs):
        self.user = kwargs['initial']['user']
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['shop'].queryset = Shop.objects.filter(user__in=[self.user.id])
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    def clean(self):
        cleaned_data = super(ProductForm, self).clean()
        title = cleaned_data.get('title', '')
        shop = cleaned_data.get('shop', '')
        category = cleaned_data.get('category', '')
        price = cleaned_data.get('price', '')
        short_description = cleaned_data.get('short_description', '')

        error_msg = "*Обязательное поле"

        if shop is None or shop == "":
            self._errors['shop'] = error_msg
        if title is None or title == "":
            self._errors['title'] = error_msg
        if category is None or category == "":
            self._errors['category'] = error_msg
        if price is None or price == "":
            self._errors['price'] = error_msg
        if short_description is None or short_description == "":
            self._errors['short_description'] = error_msg



class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['objects', 'sell_count', 'counter']

    section = forms.ModelChoiceField(queryset=GlobalCategory.objects.all())
    parent_categories = forms.ModelChoiceField(queryset=Category.objects.filter(parent=None))
    removed_images = forms.CharField(required=False)
    uploaded_images = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs['initial']['user']
        super(ProductUpdateForm, self).__init__(*args, **kwargs)
        self.fields['shop'].queryset = Shop.objects.filter(user__in=[self.user.id])
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class ProductSearchForm(SearchForm):
    models = [Product]

    def get_models(self):
        return self.models

    def search(self):
        sqs = super(ProductSearchForm, self).search().models(*self.get_models())
        return sqs


class ShopSearchForm(SearchForm):
    models = [Shop]

    def get_models(self):
        return self.models

    def search(self):
        sqs = super(ShopSearchForm, self).search().models(*self.get_models())
        return sqs


class ProductImagesForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']

