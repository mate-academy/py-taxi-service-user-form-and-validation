import re
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Car


User = get_user_model()
LICENSE_RE = re.compile(r"^[A-Z]{3}\d{5}$")


class LicenseValidationMixin:
    def clean_license_number(self):
        value = self.cleaned_data["license_number"].strip().upper()
        if not LICENSE_RE.fullmatch(value):
            raise forms.ValidationError(
                "The license number must be 8 characters long: "
                "3 uppercase Latin letters followed by 5 digits "
                "(e.g., ABC12345)."
            )
        return value


class DriverCreationForm(LicenseValidationMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "license_number")


class DriverLicenseUpdateForm(LicenseValidationMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ["license_number"]


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
