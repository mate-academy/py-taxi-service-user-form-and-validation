from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Driver, Car


class DriverCreateForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = (
            "username",
            "email",
            "license_number",
            "password1",
            "password2"
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if check_license_number(license_number):
            return license_number
        raise ValidationError("Invalid license number")


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if check_license_number(license_number):
            return license_number
        raise ValidationError("Invalid license number")


def check_license_number(license_number) -> bool:
    if (
        len(license_number) == 8
        and license_number[:3].isupper()
        and license_number[:3].isalpha()
        and license_number[-5:].isdigit()
    ):
        return True
    return False


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
