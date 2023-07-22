from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    MIN_CHARACTERS = 8
    UPPER_CHARACTERS = 3
    DIGITS = 5

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != DriverLicenseUpdateForm.MIN_CHARACTERS:
            raise ValidationError("License number must "
                                  "consist only of 8 characters")

        if (license_number[:DriverLicenseUpdateForm.UPPER_CHARACTERS]
                != license_number[
                :DriverLicenseUpdateForm.UPPER_CHARACTERS].upper()):
            raise ValidationError("First 3 must be in uppercase")
        for letter in license_number[
                :DriverLicenseUpdateForm.UPPER_CHARACTERS]:
            if letter.isdigit():
                raise ValidationError("First 3 must be in uppercase")

        for letter in license_number[DriverLicenseUpdateForm.DIGITS - 2:]:
            if not letter.isdigit():
                raise ValidationError("Last 5 must be digits")

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers",)
