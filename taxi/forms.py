from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Driver, Car


class DriverUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)


def validate_license_number(license_number: str):
    if len(license_number) != 8:
        raise ValidationError("License number must be 8 characters long.")

    chars_symbols = license_number[:3]
    chars_digits = license_number[-5:]

    if (not chars_symbols.isupper()
            or not chars_symbols.isalpha()
            or not chars_digits.isdigit()):

        raise ValidationError(
            "The first 3 symbols must be a letter UPPERCASE "
            "and 5 the end symbols must be a digit."
        )

    return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
