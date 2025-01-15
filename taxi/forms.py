from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError
from taxi.models import Driver, Car


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


def validate_license_number(license_number: str) -> str:

    if len(license_number) != 8:
        raise ValidationError("License must consist only of 8 characters")
    elif not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise ValidationError(
            "First 3 characters of license are not uppercase or letters"
        )
    elif not license_number[3:].isdigit():
        raise ValidationError("Last 5 characters are not digits")
    return license_number
