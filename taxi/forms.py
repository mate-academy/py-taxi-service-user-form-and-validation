from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError("License number should consist of 8 characters")

    first_part = license_number[:3]
    last_part = license_number[3:]

    if not (first_part.isalpha() and first_part.isupper()):
        raise ValidationError("First 3 characters should be uppercase")

    if not last_part.isdigit():
        raise ValidationError("Last 5 characters should be digits")

    return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "license_number", "first_name", "last_name",
        )

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
