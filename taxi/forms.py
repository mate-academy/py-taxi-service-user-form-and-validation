from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator, MaxLengthValidator

from taxi.models import Driver, Car


def validate_license():
    license_number = forms.CharField(
        validators=[
            RegexValidator(
                r"[A-Z]{3}[0-9]{5}",
                "Please ensure the license number format is XXX0000,"
                "where X is a capital letter and 0 is a digit",
            ),
            MaxLengthValidator(8, "License number should be 8 characters max")
        ]
    )
    return license_number


class DriverCreationForm(UserCreationForm):
    license_number = validate_license()

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = validate_license()

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):

    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
