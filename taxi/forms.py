from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError(
                "Invalid license number. It must be 8 chars."
            )

        for char in license_number[:3]:
            if not char.isalpha() or char != char.upper():
                raise ValidationError(
                    "Invalid license number. "
                    "First three chars have to be uppercase letters."
                )

        for char in license_number[3:]:
            if not char.isnumeric():
                raise ValidationError(
                    "Invalid license number. "
                    "Last five chars have to be digits."
                )

        return license_number


class DriverCreateForm(DriverLicenseUpdateForm):
    class Meta:
        model = Driver
        fields = ("username", "first_name", "last_name", "license_number")


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Car
        fields = "__all__"
