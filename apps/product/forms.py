from django import forms
from haystack.forms import SearchForm

from apps.shop.models import Shop
from .models import Product


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


class ProductSearchForm(SearchForm):
    def no_query_found(self):
        return self.searchqueryset.all()
