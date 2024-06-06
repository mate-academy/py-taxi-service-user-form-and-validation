import re

from django import forms
from taxi.models import Driver


class DriverCreateForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "First Name"})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Last Name"})
    )

    class Meta:
        model = Driver
        fields = ["username"]


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        """
        Validates the license number format.
        The license number must consist of 3 uppercase
         letters followed by 5 digits.
        Raises:
            forms.ValidationError:
            If the license number does not match the required format.
        """
        license_number = self.cleaned_data["license_number"]
        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise forms.ValidationError(
                "License number must consist of 3 uppercase"
                " letters followed by 5 digits."
            )

        return license_number
