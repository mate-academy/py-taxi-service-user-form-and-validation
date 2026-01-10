from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


def validate_license_number(license_number, check_unique=False, instance=None):
    """Shared license number validation function"""
    license_number = license_number.strip()

    if len(license_number) != 8:
        raise (ValidationError
               ("License number must be exactly 8 characters long"))

    first_three = license_number[:3]
    last_five = license_number[3:]

    if not (first_three.isalpha() and first_three.isupper()):
        raise ValidationError("First 3 characters must be uppercase letters")

    if not (len(last_five) == 5 and last_five.isdigit()):
        raise ValidationError("Last 5 characters must be digits")

    if check_unique:
        existing_drivers = get_user_model().objects.filter(
            license_number=license_number
        )

        if instance and instance.pk:
            existing_drivers = existing_drivers.exclude(pk=instance.pk)

        if existing_drivers.exists():
            raise (ValidationError
                   ("Driver with this license number already exists"))

    return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number", "")
        return validate_license_number(
            license_number, check_unique=True, instance=self.instance
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number", "")
        return validate_license_number(
            license_number, check_unique=True, instance=self.instance
        )


class DriverUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number", "")
        return validate_license_number(
            license_number, check_unique=True, instance=self.instance
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
