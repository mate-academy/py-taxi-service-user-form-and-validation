from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Car


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise forms.ValidationError(
            "License number must consist of 8 characters"
        )

    if not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise forms.ValidationError(
            "The first 3 characters must be uppercase letters"
        )

    if not license_number[3:].isdigit():
        raise forms.ValidationError(
            "The last 5 characters must be digits"
        )


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "license_number",
            "password1",
            "password2",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
