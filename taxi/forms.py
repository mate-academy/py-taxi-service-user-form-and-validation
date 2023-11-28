from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


def validate_license_number(license_number: str) -> str:
    if len(license_number) != 8:
        raise ValidationError(
            "License number must consist only of 8 characters"
        )
    if not license_number[:3].isupper() or not license_number[:3].isalpha():
        raise ValidationError(
            "First 3 characters of license number must be uppercase letters"
        )
    if not license_number[-5:].isdigit():
        raise ValidationError(
            "Last 5 characters of license number must be digits"
        )

    return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=255,
        required=True,
        validators=[validate_license_number],
    )

    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=255,
        required=True,
        validators=[validate_license_number],
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
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
