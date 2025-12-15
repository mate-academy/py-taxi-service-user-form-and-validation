from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number(license_number):
    license_number = license_number.strip()
    first_three = license_number[:3]
    last_five = license_number[3:]

    if len(license_number) != 8:
        raise ValidationError("License number must be 8 characters long")
    if not first_three.isalpha() or not first_three.isupper():
        raise ValidationError(
            "The first 3 characters must be uppercase letters"
        )
    if not last_five.isdigit():
        raise ValidationError("The last 5 characters must be digits")


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[validate_license_number],
    )

    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[validate_license_number],
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            "username",
            "license_number",
            "first_name",
            "last_name",
            "email",
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
