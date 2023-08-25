from django import forms
from django.core.exceptions import ValidationError

from .models import Driver


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = '__all__'

    def clean_driver_license(self):
        license_number = self.cleaned_data.get('license_number')

        if len(license_number) != 8:
            raise ValidationError('Driver license must consist of 8 characters.')

        if not license_number[:3].isupper():
            raise ValidationError('First 3 characters must be uppercase letters.')

        if not license_number[3:].isdigit():
            raise ValidationError('Last 5 characters must be digits.')

        return license_number
