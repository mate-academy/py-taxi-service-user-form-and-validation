from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    CHAR_NUMBER = 8

    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != DriverLicenseUpdateForm.CHAR_NUMBER:
            raise ValidationError(
                f"The number of characters must be "
                f"{DriverLicenseUpdateForm.CHAR_NUMBER} characters!"
            )

        if (not license_number[:3].isalpha()
                or not license_number[:3].isupper()):
            raise ValidationError(
                "The first 3 characters must be letters and uppercase!"
            )

        if not license_number[3:].isdigit():
            raise ValidationError(
                "Last 5 characters must be digits!"
            )

        return license_number


class DriverCreateForm(UserCreationForm, DriverLicenseUpdateForm):
    class Meta(UserCreationForm):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers", )
