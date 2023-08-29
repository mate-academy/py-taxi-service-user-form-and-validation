from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number", )

    def clean(self):
        clean_license_number(self.cleaned_data)


def clean_license_number(cleaned_data):
    license_len = 8

    license_number = cleaned_data["license_number"]

    if len(license_number) != license_len:
        raise ValidationError("License must consist only of 8 characters")

    if not license_number[:3].isupper() or not license_number[:3].isalpha():
        raise ValidationError("First 3 characters must be uppercase letters")

    if not license_number[3:].isnumeric():
        raise ValidationError("Last 5 characters must be digits")

    return license_number


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean(self):
        clean_license_number(self.cleaned_data)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
