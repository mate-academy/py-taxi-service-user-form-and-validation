from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseValidatorMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError(
                "License number should consist of 8 characters"
            )
        if (license_number[:3].upper() != license_number[:3]
                or not license_number[:3].isalpha()):
            raise ValidationError(
                "First 3 characters should be uppercase letters"
            )
        if not license_number[-5:].isnumeric():
            raise ValidationError(
                "Last 5 characters should be numbers"
            )
        return license_number


class DriverCreationForm(UserCreationForm, DriverLicenseValidatorMixin):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number"
        )


class DriverLicenseUpdateForm(forms.ModelForm, DriverLicenseValidatorMixin):
    class Meta:
        model = Driver
        fields = ["license_number", ]


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
