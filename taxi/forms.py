from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError(
            "License number have to consist only of 8 characters"
        )
    if not (license_number[0:3].isupper() and license_number[0:3].isalpha()):
        raise ValidationError(
            "First 3 characters have to be uppercase letters"
        )
    if not license_number[3:].isdigit():
        raise ValidationError(
            "Last 5 characters have to be digits"
        )
    return license_number


class DriverForm(forms.ModelForm):
    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)
