from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm, forms.ModelForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        return clean_license_number_func(license_number)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        return clean_license_number_func(license_number)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"


def clean_license_number_func(license_number: str) -> str:
    if len(license_number) == 8:
        if license_number[3:].isdigit():
            if license_number[:3].isalpha():
                if license_number[:3].isupper():
                    return license_number

    raise ValidationError(
        "License Number mist be 8 characters long: first 3 are "
        "uppercase letters and last 5 are digits"
    )
