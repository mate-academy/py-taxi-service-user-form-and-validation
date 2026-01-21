from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def clean_license_number(license_number: str) -> str:
    license_length = 8
    split_index = 3
    letters_length = split_index
    digits_length = license_length - split_index

    if len(license_number) != license_length:
        raise ValidationError(
            f"Ensure that license consists of {license_length} characters"
        )

    if (not license_number[:split_index].isalpha()
            or not license_number[:split_index].isupper()):
        raise ValidationError(
            f"Ensure that the first {letters_length} "
            f"characters are uppercase letters"
        )

    if not license_number[split_index:].isdigit():
        raise ValidationError(
            f"Ensure that the last {digits_length} characters are digits"
        )

    return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )

    def clean_license_number(self) -> str:
        return clean_license_number(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        return clean_license_number(self.cleaned_data["license_number"])


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta(UserCreationForm.Meta):
        model = Car
        fields = "__all__"
