from django import forms
from .models import ProductReviews, ShopReviews

class ProductReviewsForm(forms.ModelForm):
    class Meta:
        model = ProductReviews
        exclude = ['user']

    rating = forms.CharField(required=False)
