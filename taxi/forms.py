from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Car

User = get_user_model()


def validate_license_number(license_number):
    if (
        len(license_number) != 8
        or not license_number[:3].isalpha()
        or not license_number[:3].isupper()
        or not license_number[3:].isdigit()
    ):
        raise forms.ValidationError(
            "License number must consist of 3 uppercase letters and 5 digits"
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = User   # 🔥 FIX
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User   # 🔥 FIX
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
