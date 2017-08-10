from django.forms import ModelChoiceField


class CustomField(ModelChoiceField):

    def validate(self, value):
        pass
