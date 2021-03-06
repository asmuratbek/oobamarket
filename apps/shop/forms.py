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

    def clean(self):
        cleaned_data = super(ShopForm, self).clean()
        title = cleaned_data.get('title', '')
        email = cleaned_data.get('email', '')
        short_desc = cleaned_data.get('short_description')

        error_msg = "*Обязательное поле"

        if title is None or title == "":
            self._errors['title'] = error_msg
        if email is None or email == "":
            self._errors['email'] = error_msg
        if len(short_desc) > 300:
            self._errors['short_description'] = "Вы превысили допустимое количество символов"







class ShopBannersForm(ModelForm):
    class Meta:
        model = Banners
        fields = ['image',]


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

    def clean_facebook(self):
        facebook = self.cleaned_data.get('facebook')
        if not 'facebook' and '' in facebook:
            raise forms.ValidationError('Пожалуйста введите корректную ссылку с фейсбука')
        return facebook

    def clean_vk(self):
        vk = self.cleaned_data.get('vk')
        if not 'vk' and '' in vk:
            raise forms.ValidationError('Пожалуйста введите корректную ссылку с vk')
        return vk

    def clean_twitter(self):
        twitter = self.cleaned_data.get('twitter')
        if not 'twitter' and '' in twitter:
            raise forms.ValidationError('Пожалуйста введите корректную ссылку с twitter')
        return twitter


    def clean_instagram(self):
        instagram = self.cleaned_data.get('instagram')
        if not 'instagram' and '' in instagram:
            raise forms.ValidationError('Пожалуйста введите корректную ссылку с instagram')
        return instagram




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

