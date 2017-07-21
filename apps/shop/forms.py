from django.forms import ModelForm, forms, inlineformset_factory
from .models import Shop, Banners, SocialLinks, Contacts, Sales


# class ShopForm(ModelForm):
#     # class Meta:
#     #     model = Shop
#     #     fields = ['title', 'logo', 'email', 'phone', 'short_description', 'description', 'user', 'slug',]


class ShopForm(ModelForm):
    class Meta:
        model = Shop
        exclude = ['user', 'slug', 'counter']

    def __init__(self, *args, **kwargs):
        super(ShopForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    def clean_logo(self):
        logo = self.cleaned_data['logo']
        if not logo:
            raise forms.ValidationError("Логотип обязателен для заполнения", code='no_logo')
        return logo


class ShopBannersForm(ModelForm):
    class Meta:
        model = Banners
        fields = ['title', 'image']


class ShopSocialLinksForm(ModelForm):
    class Meta:
        model = SocialLinks
        exclude = ['shop']

    def __init__(self, *args, **kwargs):
        super(ShopSocialLinksForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class ShopContactInline(ModelForm):
    class Meta:
        model = Contacts
        fields = ('published', 'phone', 'address', 'shop')


ShopInlineFormSet = inlineformset_factory(Shop, Contacts, extra=1,
                                          fields=(
                                              'published', 'phone', 'address', 'place', 'latitude',
                                              'longitude', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                                              'saturday', 'sunday'), can_delete=True)


class SalesCreateForm(ModelForm):
    class Meta:
        model = Sales
        exclude = ['shop']
