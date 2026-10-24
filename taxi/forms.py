from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = ("username", "password1", "password2", "license_number")

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data.get("license_number")
        if len(license_number) == 8:
            if (license_number[:3].isalpha()
                    and license_number[:3] == license_number[:3].upper()
                    and license_number[3:].isnumeric()):
                return license_number
        raise ValidationError("Not valid")


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data.get("license_number")
        if len(license_number) == 8:
            if (license_number[:3].isalpha()
                    and license_number[:3] == license_number[:3].upper()
                    and license_number[3:].isnumeric()):
                return license_number
        raise ValidationError("Not valid")


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
