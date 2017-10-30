from django import forms
from django.contrib.auth import get_user_model

from .models import UserAddress, SimpleOrder

User = get_user_model()


class GuestCheckoutForm(forms.Form):
    email = forms.EmailField()
    email2 = forms.EmailField(label='Verify Email')

    def clean_email2(self):
        email = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")

        if email == email2:
            user_exists = User.objects.filter(email=email).count()
            if user_exists != 0:
                raise forms.ValidationError("This User already exists. Please login instead.")
            return email2
        else:
            raise forms.ValidationError("Please confirm emails are the same")


class AddressForm(forms.Form):
    billing_address = forms.ModelChoiceField(
        queryset=UserAddress.objects.filter(type="billing"),
        widget=forms.RadioSelect,
        empty_label=None
    )
    shipping_address = forms.ModelChoiceField(
        queryset=UserAddress.objects.filter(type="shipping"),
        widget=forms.RadioSelect,
        empty_label=None,

    )


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = [
            'street',
            'city',
            'type'
        ]


class SimpleOrderForm(forms.ModelForm):
    class Meta:
        model = SimpleOrder
        fields = [
            'name',
            'last_name',
            'phone',
            'address',
        ]

    def __init__(self, *args, **kwargs):
        super(SimpleOrderForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(SimpleOrderForm, self).clean()
        name = cleaned_data.get('name', '')
        last_name = cleaned_data.get('last_name', '')
        phone = cleaned_data.get('phone', '')
        address = cleaned_data.get('address', '')

        error_msg = "*Обязательное поле"

        if name is None or name == "":
            self._errors['name'] = error_msg
        if last_name is None or last_name == "":
            self._errors['last_name'] = error_msg
        if phone is None or phone == "":
            self._errors['phone'] = error_msg
        if address is None or address == "":
            self._errors['address'] = error_msg


class ShopSimpleOrderForm(forms.ModelForm):
    class Meta:
        model = SimpleOrder
        fields = [
            'status',
            'comments',
        ]

    def __init__(self, *args, **kwargs):
        super(ShopSimpleOrderForm, self).__init__(*args, **kwargs)
        # self.status = kwargs['initial']['status']
