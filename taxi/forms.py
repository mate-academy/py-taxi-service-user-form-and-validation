from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Car


def validate_license_number(license_number: str) -> str:
    license_number = (license_number or "").strip()

    if len(license_number) != 8:
        raise ValidationError(
            "License number must have exactly 8 characters")

    first_part = license_number[:3]
    if not (first_part.isalpha() and first_part.isupper()):
        raise ValidationError(
            "First 3 characters must be uppercase letters (A–Z)")

    last_part = license_number[-5:]
    if not last_part.isdigit():
        raise ValidationError("Last 5 characters must be digits (0–9)")

    return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        validate_license_number(self.cleaned_data.get("license_number"))


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        validate_license_number(self.cleaned_data.get("license_number"))


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
