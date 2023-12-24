from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.forms import CheckboxSelectMultiple

from taxi.models import Driver, Car


class CleanMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError("license number should be 8 characters")
        is_digit = str.isdigit
        if any(map(is_digit, license_number[:3])):
            raise ValidationError(
                "first 3 characters have to be letters")
        if license_number[:3].upper() != license_number[:3]:
            raise ValidationError(
                "first 3 characters have to be uppercase letters")
        if not all(map(is_digit, license_number[-5:])):
            raise ValidationError("Last 5 characters have to be digits")
        return license_number


class UserCreationForm(CleanMixin, UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverLicenseUpdateForm(CleanMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)
