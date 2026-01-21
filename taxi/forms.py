from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validator_license_number(value: str):
    """
    Validates a driver's license number.

    The license number must follow these rules:
    - It must be exactly 8 characters long.
    - The first 3 characters must be uppercase letters.
    - The last 5 characters must be digits.

    Args:
        value (str): The license number to validate.

    Returns:
        str: The valid license number if all conditions are met.

    Raises:
        ValidationError: If the license number does not
         match the required format.
    """
    valid_length = 8
    license_number = value
    valid_chars = all(
        [license_number[:3].isalpha(),
         license_number[:3] == license_number[:3].upper()]
    )
    valid_digits = license_number[3:].isdigit()
    if len(license_number) == valid_length and valid_chars and valid_digits:
        return license_number
    raise ValidationError(
        """
    The license number must be 8 characters long,
    The first 3 characters are capital letters,
    The last 5 characters are numbers,
    """
    )


class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        max_length=8,
        validators=[validator_license_number]
    )

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        max_length=8,
        validators=[validator_license_number]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
