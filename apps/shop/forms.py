from django.forms import ModelForm, forms, inlineformset_factory
from .models import Shop, Banners, SocialLinks, Contacts, Sales




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

    def clean(self):
        cleaned_data = super(ShopForm, self).clean()
        # title = cleaned_data.get('title', '')
        email = cleaned_data.get('email', '')

        error_msg = "*Обязательное поле"

        # if title is None or title == "":
        #     self._errors['title'] = error_msg
        if email is None or email == "":
            self._errors['email'] = error_msg





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


ShopInlineFormSet = inlineformset_factory(Shop, Contacts, extra=1, max_num=1,
                                          fields=(
                                              'published', 'phone', 'address', 'place', 'latitude',
                                              'longitude', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                                              'saturday', 'sunday', 'round_the_clock'), can_delete=True)


class SalesCreateForm(ModelForm):
    class Meta:
        model = Sales
        exclude = ['shop']

