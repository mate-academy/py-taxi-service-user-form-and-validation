import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from taxi.models import Driver, Car


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class LicenseNumberMixin(forms.ModelForm):
    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if license_number and not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise forms.ValidationError(
                "Invalid number: lens must be 8 characters, "
                "first 3 characters are uppercase letters, "
                "last 5 characters are digits"
            )
        return license_number


class DriverLicenseUpdateForm(LicenseNumberMixin, forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("license_number",)


class DriverCreationForm(LicenseNumberMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number"
        )
