from django import forms
from .models import ProductReviews, ShopReviews


class AbstractReviewsForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=(
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)
    ), initial=3)


class ProductReviewsForm(AbstractReviewsForm):
    class Meta:
        model = ProductReviews
        exclude = ['user']


class ShopReviewsForm(AbstractReviewsForm):
    class Meta:
        model = ShopReviews
        exclude = ['user']


