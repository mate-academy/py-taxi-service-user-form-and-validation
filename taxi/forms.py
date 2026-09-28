import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from taxi.models import Car


def validate_license_number(license_number: str) -> str | ValidationError:
    if len(license_number) != 8:
        raise ValidationError("License number must "
                              "consist of exactly 8 characters.")
    if not re.fullmatch(r"[A-Z]{3}", license_number[:3]):
        raise ValidationError("The first 3 characters "
                              "must be uppercase letters.")
    if not re.fullmatch(r"[0-9]{5}", license_number[3:]):
        raise ValidationError("The last 5 characters must be digits.")
    return license_number


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["license_number"]

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class CarForm(ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
