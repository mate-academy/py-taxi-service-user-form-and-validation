from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


def valid_license_number(license_number):
    if (len(license_number) != 8
            or not license_number[0:3].isalpha()
            or not license_number[0:4].isupper()
            or not license_number[-5:].isnumeric()):
        raise ValidationError("Incorrect license number")
    return license_number


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        validators=[valid_license_number]
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        validators=[valid_license_number]
    )

    class Meta:
        model = get_user_model()
        fields = ("license_number", )


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
