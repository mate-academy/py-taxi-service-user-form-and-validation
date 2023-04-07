from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class LicenseNumberMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError("License number must have 8 characters.")

        if not license_number[:3].isupper():
            raise ValidationError(
                "First 3 letters of license number must be uppercase."
            )

        if not license_number[3:].isnumeric():
            raise ValidationError(
                "Last 5 characters of license number must be digits."
            )

        return license_number


class DriverForm(UserCreationForm, LicenseNumberMixin):

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number", "first_name", "last_name"
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
