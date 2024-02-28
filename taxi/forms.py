from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Driver, Car


def validate_license_number(license_number):
    license_len = 8
    start_letters_count = 3
    last_numbers_count = 5
    if len(license_number) != license_len:
        raise ValidationError(
            f"License number must be {license_len} characters long."
        )
    if not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise ValidationError(
            f"First {start_letters_count} characters must be uppercase letters."
        )
    if not license_number[3:].isdigit():
        raise ValidationError(
            f"Last {last_numbers_count} characters must be digits."
        )


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self) -> None:
        license_number = self.cleaned_data.get("license_number")
        validate_license_number(license_number)
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self) -> None:
        license_number = self.cleaned_data.get("license_number")
        validate_license_number(license_number)
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
