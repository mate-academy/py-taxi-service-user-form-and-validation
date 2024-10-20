from django import forms

from taxi.models import Car, Driver
from taxi.validators import LicenseNumberValidator


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        label="Driver's License",
        validators=[LicenseNumberValidator()],
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
