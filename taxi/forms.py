from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Driver, Car


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields = ("license_number", )

    def clean_license_number(self):
        return check_license_number(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        return check_license_number(self.cleaned_data["license_number"])


def check_license_number(license_number: str) -> str | ValidationError:
    text = ("License number should consist of first "
            "3 uppercase letters and 5 digits")
    if len(license_number) != 8 or not license_number[:3].isupper():
        raise ValidationError(text)
    if not license_number[:3].isalpha() or not license_number[3:].isdigit():
        raise ValidationError(text)
    return license_number
