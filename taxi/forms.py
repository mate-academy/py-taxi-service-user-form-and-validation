from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = (
            "license_number",
            "email",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not len(license_number) == 8:
            raise ValidationError(
                "The license number must be 8 characters long"
            )
        if (
            not license_number[:3].isalpha()
            or not license_number[:3].isupper()
        ):
            raise ValidationError(
                "The first 3 characters must be uppercase letters."
            )
        if not license_number[3:].isdigit():
            raise ValidationError("The last 5 characters must be digits.")
        return license_number


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
