from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number(license_number: str) -> str:
    if len(license_number) != 8:
        raise ValidationError("The length should be 8 characters")
    if not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise ValidationError("The first 3 characters must be capital letters")
    if not license_number[3:].isdigit():
        raise ValidationError("The last 5 characters must be numbers")

    return license_number


class DriverCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        data = self.cleaned_data["license_number"]
        validate_license_number(data)
        return data


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        data = self.cleaned_data["license_number"]
        validate_license_number(data)
        return data


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
