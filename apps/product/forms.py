from django import forms
from haystack.forms import SearchForm

from apps.category.models import Category
from apps.global_category.models import GlobalCategory
from apps.shop.models import Shop
from .models import Product, ProductImage


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['slug', 'objects', 'sell_count']

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


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['objects', 'sell_count']

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

