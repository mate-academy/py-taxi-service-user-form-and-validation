from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError(
                "The license number must be exactly 8 characters long."
            )
        elif not license_number[:3].isalpha() \
                or not license_number[:3].isupper():
            raise ValidationError(
                "The first three characters must be uppercase letters."
            )
        elif not license_number[3:].isdigit():
            raise ValidationError(
                "The last five characters must be digits."
            )

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
