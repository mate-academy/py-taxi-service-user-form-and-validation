from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car
from django import forms


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):

    LEN_LICENCE = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != DriverLicenseUpdateForm.LEN_LICENCE:
            raise ValidationError(
                f"Ensure that lisense consists of "
                f"{DriverLicenseUpdateForm.LEN_LICENCE} characters."
            )

        if not (license_number[:3].isalpha() and license_number[:3].isupper()):
            raise ValidationError(
                "Ensure that first 3 characters are uppercase letters."
            )

        if not license_number[4:].isdigit():
            raise ValidationError(
                "Ensure that last 5 characters are digits."
            )

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer")
