from django.forms import ModelForm, forms
from .models import Shop, Banners, SocialLinks


# class ShopForm(ModelForm):
#     # class Meta:
#     #     model = Shop
#     #     fields = ['title', 'logo', 'email', 'phone', 'short_description', 'description', 'user', 'slug',]


class ShopForm(ModelForm):
    class Meta:
        model = Shop
        exclude = ['user', 'slug']

    def __init__(self, *args, **kwargs):
        super(ShopForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    def clean_logo(self):
        logo = self.cleaned_data['logo']
        if not logo:
            raise forms.ValidationError("Логотип обязателен для заполнения")
        return logo

class ShopBannersForm(ModelForm):
    class Meta:
        model = Banners
        fields = ['title', 'image']

    # def __init__(self, *args, **kwargs):
    #     super(ShopBannersForm, self).__init__(*args, **kwargs)
    #     for field in iter(self.fields):
    #         self.fields[field].widget.attrs.update({
    #             'class': 'form-control'
    #         })

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
