import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if not re.fullmatch(r"[A-Z]{3}\d{5}", license_number):
            raise forms.ValidationError("Invalid license number")
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        if len(self.cleaned_data["license_number"]) != 8:
            raise ValidationError("License number"
                                  " must be"
                                  " 8 characters long")
        if (
            not self.cleaned_data["license_number"][:3].isalpha()
            or not self.cleaned_data["license_number"][:3].isupper()
        ):
            raise ValidationError("First 3"
                                  " characters must be uppercase letters")
        if not self.cleaned_data["license_number"][-5:].isdigit():
            raise ValidationError("Last 5 characters must be digits")
        return self.cleaned_data["license_number"]


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
