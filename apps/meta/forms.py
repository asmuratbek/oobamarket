from django.forms import ModelForm
from .models import Claim


class ClaimForm(ModelForm):
    class Meta:
        model = Claim
        fields = ['name', 'phone']

    msg_limit = "Превышено допустимое количество символов"
    msg_null = "Поле не может быть пустым"

    def clean(self):
        cleaned_data = super(ClaimForm, self).clean()
        name = cleaned_data.get("name")
        phone = cleaned_data.get("phone")
        if name and phone:
            if len(name) >= 300:
                self._errors["name"] = self.msg_limit
            if len(phone) >= 255:
                self._errors["phone"] = self.msg_limit
        if name is None or name == "":
            self._errors["name"] = self.msg_null
        if phone is None or phone == "":
            self._errors["phone"] = self.msg_null
