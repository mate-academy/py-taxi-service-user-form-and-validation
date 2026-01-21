from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    LICENSE_LEN = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):

        license_number = self.cleaned_data["license_number"]

        if len(license_number) != DriverLicenseUpdateForm.LICENSE_LEN:
            raise ValidationError(
                "License number must contain "
                f"{DriverLicenseUpdateForm.LICENSE_LEN} characters")

        if (not license_number[0:3].isalpha()
                or not license_number[0:3].isupper()):
            raise ValidationError(
                "First 3 characters should be uppercase letters")

        if not license_number[3:8].isnumeric():
            raise ValidationError(
                "Last 5 characters should be digits")

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
