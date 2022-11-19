from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
            "email",
        )

    def clean_license_number(self):
        validate_license_number(self.cleaned_data["license_number"])
        return self.cleaned_data["license_number"]


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        validate_license_number(self.cleaned_data["license_number"])
        return self.cleaned_data["license_number"]


def validate_license_number(cleaned_data):
    license_number = cleaned_data
    if len(license_number) != 8:
        raise ValidationError("License number must consist only 8 characters")
    if not license_number[:3].isupper():
        raise ValidationError("First 3 characters must be uppercase")
    if not license_number[3:].isdigit():
        raise ValidationError("Last 5 characters must be digits")

    return license_number
