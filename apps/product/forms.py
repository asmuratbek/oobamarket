from django import forms
from haystack.forms import SearchForm

from .fields import CustomField
from apps.category.models import Category
from apps.global_category.models import GlobalCategory
from apps.shop.models import Shop
from .models import Product, ProductImage


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['slug', 'objects', 'sell_count', 'counter']

    section = forms.ModelChoiceField(queryset=GlobalCategory.objects.filter(published=True))
    parent_categories = CustomField(queryset=Category.objects.filter(parent=None))
    removed_images = forms.CharField(required=False)
    uploaded_images = forms.CharField(required=False)


    def __init__(self, *args, **kwargs):
        self.user = kwargs['initial']['user']
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['shop'].queryset = Shop.objects.filter(user__in=[self.user.id])
        self.fields.get('parent_categories').widget.attrs['disabled'] = True
        self.fields.get('category').widget.attrs['disabled'] = True

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

        error_msg = "*Обязательное поле"

        if shop is None or shop == "":
            self._errors['shop'] = error_msg
        if title is None or title == "":
            self._errors['title'] = error_msg
        if category is None or category == "":
            self._errors['category'] = error_msg
        if price is None or price == "":
            self._errors['price'] = error_msg


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['objects', 'slug', 'sell_count', 'counter']

    section = forms.ModelChoiceField(queryset=GlobalCategory.objects.filter(published=True))
    parent_categories = forms.ModelChoiceField(queryset=Category.objects.filter(parent=None))
    removed_images = forms.CharField(required=False)
    uploaded_images = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs['initial']['user']
        super(ProductUpdateForm, self).__init__(*args, **kwargs)
        # self.fields['shop'].queryset = Shop.objects.filter(user__in=[self.user.id])
        # self.fields['parent_categories'].queryset = Category.objects.filter(parent=None, section__id=kwargs.get('initial')['section'])
        # self.fields['category'].queryset = Category.objects.get(id=kwargs.get("initial")['parent_categories']).get_descendants()
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class ProductImagesForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']


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
