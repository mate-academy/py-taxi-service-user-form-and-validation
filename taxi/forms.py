from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator

from taxi.models import Driver, Car


class BaseForm(forms.ModelForm):
    MAX_LENGTH = 8
    license_number = forms.CharField(
        validators=[
            MaxLengthValidator(MAX_LENGTH),
        ]
    )

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if not license_number[-5:].isdigit():
            raise forms.ValidationError("last 5 char must be digits")
        elif (license_number[0:3].isalpha() is False
              or not license_number[0:3].isupper()):
            raise forms.ValidationError("first 3 char must be uppercase")
        return license_number


# not license_number[0:3].isupper():

class DriverLicenseUpdateForm(BaseForm):
    class Meta:
        model = Driver
        fields = ("license_number",)


class DriverCreateForm(BaseForm):
    class Meta:
        model = Driver
        fields = (
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "license_number",
        )


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
