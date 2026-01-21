from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def clean_license_number(cleaned_data):
    license_number = cleaned_data["license_number"]
    three_first_chars = license_number[0:3]
    last_5_chars = license_number[-5:]
    if len(license_number) != 8:
        raise ValidationError(
            "Ensure that length of license number is 8"
        )
    elif not three_first_chars.isalpha() or not three_first_chars.isupper():
        raise ValidationError(
            "Ensure that First 3 characters are uppercase letters"
        )
    elif not last_5_chars.isdigit():
        raise ValidationError(
            "Ensure that Last 5 characters are digits"
        )
    return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = (
            UserCreationForm.Meta.fields
            + ("first_name", "last_name", "license_number")
        )

    def clean_license_number(self):
        return clean_license_number(self.cleaned_data)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        return clean_license_number(self.cleaned_data)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
