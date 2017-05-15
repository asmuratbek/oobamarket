from django.forms import ModelForm
from .models import Product
from haystack.forms import SearchForm


class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ['slug', 'objects']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class ProductSearchForm(SearchForm):

    def no_query_found(self):
        return self.searchqueryset.all()