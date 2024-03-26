from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number(lic_number):
    if len(lic_number) != DriverCreationForm.MAX_LICENSE_NUM_LENGTH:
        raise ValidationError("Ensure the value has length 8 characters")

    if not (lic_number[0:DriverCreationForm.FIRST_CHARS_LICE_NUM].isupper()
       and lic_number[0:DriverCreationForm.FIRST_CHARS_LICE_NUM].isalpha()):
        raise ValidationError(f"Ensure the first "
                              f"{DriverCreationForm.FIRST_CHARS_LICE_NUM} "
                              f"are uppercase letters"
                              )

    if not lic_number[DriverCreationForm.FIRST_CHARS_LICE_NUM:
                      DriverCreationForm.FIRST_CHARS_LICE_NUM
                      + DriverCreationForm.LAST_CHAR_LICE_NUM].isdigit():
        raise ValidationError(f"Ensure the last "
                              f"{DriverCreationForm.LAST_CHAR_LICE_NUM} "
                              f"characters are digits"
                              )

    return lic_number


class DriverCreationForm(UserCreationForm):
    MAX_LICENSE_NUM_LENGTH = 8
    FIRST_CHARS_LICE_NUM = 3
    LAST_CHAR_LICE_NUM = 5

    license_number = forms.CharField(
        max_length=255,
        validators=[validate_license_number]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "username",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    MAX_LICENSE_NUM_LENGTH = 8
    FIRST_CHARS_LICE_NUM = 3
    LAST_CHAR_LICE_NUM = 5

    license_number = forms.CharField(
        max_length=255,
        validators=[validate_license_number]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = (
            "license_number",
        )


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
