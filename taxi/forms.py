from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if not (
            license_number[:3].isupper()
            and license_number[:3].isalpha()
            and license_number[3:].isdigit()
        ):
            raise ValidationError(
                "Ensure that the value consists of three"
                " uppercase letters followed by five"
                " digits (e.g., 'AAA12345')."
            )
        return license_number
