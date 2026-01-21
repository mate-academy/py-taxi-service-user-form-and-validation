import re

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Car


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


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
        pattern = r"^[A-Z]{3}\d{5}$"
        match = re.match(pattern, license_number)
        if not match:
            raise ValidationError(
                "You put wrong format of license_number! "
                "It should have the next format: 'ABC12345'"
            )
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        pattern = r"^[A-Z]{3}\d{5}$"
        match = re.match(pattern, license_number)
        if not match:
            raise ValidationError(
                "You put wrong format of license_number! "
                "It should have the next format: 'ABC12345'"
            )
        return license_number
