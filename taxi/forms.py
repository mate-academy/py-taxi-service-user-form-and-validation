from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    drivers = forms.CharField

    class Meta:
        model = Driver
        fields = ("first_name", "last_name", "username", "license_number", "password")

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if (len(license_number) == 8
                and license_number[:3].isalpha()
                and license_number[:3].isupper()
                and license_number[3:].isdigit()):
            return license_number

        raise ValidationError(
            "Please enter a valid license number."
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
