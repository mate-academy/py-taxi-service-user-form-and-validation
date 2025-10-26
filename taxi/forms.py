from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


class LicenseValidationMixin:
    def clean(self):
        cleaned_data = super().clean()
        license_number = cleaned_data.get("license_number")
        if license_number and (
            len(license_number) != 8
            or not license_number[:3].isalpha()
            or not license_number[:3].isupper()
            or not license_number[3:].isdigit()
        ):
            raise ValidationError("Enter correct license number")
        return cleaned_data


class DriverCreateForm(LicenseValidationMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(LicenseValidationMixin, forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["license_number"]


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple,
        }
