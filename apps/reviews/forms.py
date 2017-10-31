from django import forms
from .models import ProductReviews, ShopReviews


class ProductReviewsForm(forms.ModelForm):
    class Meta:
        model = ProductReviews
        exclude = ['user']

    rating = forms.CharField(required=False)


class ShopReviewsForm(forms.ModelForm):
    class Meta:
        model = ShopReviews
        exclude = ['user']

    rating = forms.ChoiceField(choices=(
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)
    ), initial=3)
