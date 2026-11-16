from django import forms
from django.core.validators import RegexValidator

from taxi.models import Driver, Car

license_validator = RegexValidator(
    regex=r"^[A-Z]{3}\d{5}$",
    message="License must contain 3 uppercase letters followed by 5 digits.",
)


class DriverCreationForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[license_validator]
    )

    class Meta:
        model = Driver
        fields = "__all__"


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[license_validator]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarCreationForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple,
        }
