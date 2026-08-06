from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license(driver_license):
    if len(driver_license) != 8:
        raise ValidationError("License must contain exactly 8 characters.")
    if not driver_license[:3].isalpha():
        raise ValidationError("First 3 characters must be letters.")
    if not driver_license[:3].isupper():
        raise ValidationError("First 3 characters must be uppercase letters.")
    if not driver_license[3:].isdigit():
        raise ValidationError("Last 5 characters must be digits.")
    return driver_license


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        return validate_license(self.cleaned_data["license_number"])


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        return validate_license(self.cleaned_data["license_number"])


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
