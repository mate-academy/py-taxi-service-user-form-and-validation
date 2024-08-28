from django import forms
from .models import Driver, Car


class LicenseNumberValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if (
            len(license_number) != 8
            or not license_number[:3].isalpha()
            or not license_number[:3].isupper()
            or not license_number[3:].isdigit()
        ):
            raise forms.ValidationError(
                "License number must consist"
                " of 3 uppercase letters followed by 5 digits."
            )
        return license_number


class DriverForm(LicenseNumberValidationMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = [
            "username",
            "first_name",
            "last_name",
            "license_number",
            "email", "password"
        ]


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ["model", "manufacturer", "drivers"]
