from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Car, Manufacturer

User = get_user_model()


# 🔹 Common validator (DRY)
def validate_license_number(license_number: str):
    if len(license_number) != 8:
        raise ValidationError(
            "License number must consist of exactly 8 characters"
        )

    if not license_number[:3].isupper() or not license_number[:3].isalpha():
        raise ValidationError(
            "First 3 characters must be uppercase letters"
        )

    if not license_number[3:].isdigit():
        raise ValidationError(
            "Last 5 characters must be digits"
        )

    return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        return validate_license_number(
            self.cleaned_data["license_number"]
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("license_number",)

    def clean_license_number(self):
        return validate_license_number(
            self.cleaned_data["license_number"]
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = "__all__"
