from django import forms
from .models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if (len(license_number) != 8 or not license_number[:3].isalpha()
                or license_number[:3] != license_number[:3].upper()
                or not license_number[-5:].isdigit()):
            raise forms.ValidationError("Invalid license number")
        return license_number


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
