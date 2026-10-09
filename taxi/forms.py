from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validation_license_number(license_number):
    if not (
            len(license_number) == 8
            and (
                license_number[:3].isalpha()
                and license_number[:3].isupper()
                and license_number[3:].isdigit()
            )
    ):
        raise ValidationError(
            "Ensure that value is 8 characters, "
            "the first 3 characters are uppercase letters, "
            "and the last 5 characters are numbers"
        )
    return license_number


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=255,
        validators=[validation_license_number]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number", "first_name", "last_name",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=255,
        validators=[validation_license_number]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
