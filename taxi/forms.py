import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from taxi.models import Car, Driver
from django.contrib.auth import get_user_model


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):  # type: ignore
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (  # type: ignore
            "license_number",
            "first_name",
            "last_name",
            "email",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must be exactly 8 characters long."
            )

        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise forms.ValidationError(
                "License number must start with 3"
                "uppercase letters followed by 5 digits (e.g., ABC12345)."
            )

        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must be exactly 8 characters long."
            )

        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise forms.ValidationError(
                "License number must start with 3"
                "uppercase letters followed by 5 digits (e.g., ABC12345)."
            )
        return license_number


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
