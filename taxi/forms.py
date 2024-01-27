from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError("License plate should contain 8 digits")

        if not license_number[3:].isnumeric():
            raise ValidationError("Last 5 digits should be a number")

        if (not license_number[:3].isupper()
                or not license_number[:3].isalpha()):
            raise ValidationError(
                "First 3 char should be an uppercase and a letter"
            )

        return license_number


class DriverCreationForm(DriverForm, UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "license_number",
        )


class DriverLicenseUpdateForm(DriverForm):
    pass


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
            queryset=get_user_model().objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers",)
