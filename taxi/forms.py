from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("first_name", "last_name", "license_number")

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError(
                "license number must consist only 8 characters"
            )
        if (
                license_number[:3] != license_number[:3].upper()
        ):
            raise ValidationError(
                "First 3 characters must be uppercase letters"
            )
        if not all(element.isalpha() for element in license_number[:3]):
            raise ValidationError(
                "First 3 character must be letters"
            )

        if not all(
                element.isdigit() for element in license_number[3:]
        ):
            raise ValidationError(
                "Last 5 characters must be digits"
            )
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError(
                "license number must consist only 8 characters"
            )
        if (
            license_number[:3] != license_number[:3].upper()
        ):
            raise ValidationError(
                "First 3 characters must be uppercase letters"
            )
        if not all(element.isalpha() for element in license_number[:3]):
            raise ValidationError(
                "First 3 character must be letters"
            )

        if not all(
            element.isdigit() for element in license_number[3:]
        ):
            raise ValidationError(
                "Last 5 characters must be digits"
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
