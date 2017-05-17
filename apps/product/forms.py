from django.forms import ModelForm

from apps.shop.models import Shop
from .models import Product
from haystack.forms import SearchForm


class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ['slug', 'objects']

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
