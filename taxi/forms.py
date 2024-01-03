from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver


class DriverCreateForm(UserCreationForm, forms.ModelForm):
    class Meta(UserCreationForm):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "license_number")

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        for letter in license_number[:3]:
            if letter not in "QWERTYUIOPASDFGHJKLZXCVBNM":
                raise ValidationError(f"Ensure the value of first must be 3 uppercase letter")
        for num in license_number[3:]:
            if num not in "1234567890":
                raise ValidationError(f"Ensure the value of last 5 symbols must be numbers")
        if len(license_number) != 8:
            raise ValidationError(f"Ensure the lenght of license number must be 8")
        return license_number
