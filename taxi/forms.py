from django.contrib.auth import get_user_model
from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from taxi.models import Driver


class DriverLicenseUpdateForm(forms.ModelForm):
    LENGTH = 8

    model = get_user_model()
    license_number = forms.CharField(
        required=True,
        validators=[
            MinLengthValidator(LENGTH),
            MaxLengthValidator(LENGTH),
        ]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        letters = license_number[:3]
        numbers = license_number[3:]

        if not letters.isalpha():
            raise ValidationError("First three symbols must be letters.")

        if not letters.isupper():
            raise ValidationError("Letters must be uppercase.")

        if not numbers.isdigit():
            raise ValidationError("Last five symbols must be numbers.")

        return license_number
