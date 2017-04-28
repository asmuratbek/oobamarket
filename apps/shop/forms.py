from django.forms import ModelForm
from .models import Shop


class ShopForm(ModelForm):
    model = Shop
