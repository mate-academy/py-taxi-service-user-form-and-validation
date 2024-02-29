from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        return validate_license_number(
            self.cleaned_data["license_number"]
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        return validate_license_number(
            self.cleaned_data["license_number"]
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


def validate_license_number(license_number: str) -> str | ValidationError:
    if len(license_number) != 8:
        raise ValidationError("Length of license number should be 8.")
    if not license_number[:3].isupper() or not license_number[:3].isalpha():
        raise ValidationError("License number should start with 3 uppercase letters.")
    if not license_number[3:].isdigit():
        raise ValidationError("License number should end with 5 digits.")

    return license_number
