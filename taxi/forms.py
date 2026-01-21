from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError("License Number must be 8 characters")

        if not all(char.isupper() for char in license_number[:3]):
            raise ValidationError(
                "The first three characters must be in uppercase letters."
            )

        if not all(char.isdigit() for char in license_number[-5:]):
            raise ValidationError("Last 5 characters must be numbers.")
        return license_number


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers",)
