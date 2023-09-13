from django import forms

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError(
                "Driver's license must consist of 8 characters."
            )
        if not license_number[:3].isalpha():
            raise forms.ValidationError(
                "First 3 characters of driver's license "
                "must be uppercase letters."
            )
        if not license_number[3:].isdigit():
            raise forms.ValidationError(
                "Last 5 characters of driver's license must be digits."
            )
        return license_number


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = (
            "manufacturer",
            "model",
            "drivers",
        )
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
