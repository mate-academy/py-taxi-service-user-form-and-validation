from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


def license_validation(license_number):
    if len(license_number) != 8:
        raise ValidationError(
            "length should be 8 characters"
        )
    if license_number[:3] != license_number[:3].upper():
        raise ValidationError(
            "first 3 characters should be uppercase"
        )
    if not license_number[:3].isalpha():
        raise ValidationError(
            "first 3 characters should be letters"
        )
    if not license_number[3:].isdigit():
        raise ValidationError(
            "last 5 characters should be digits"
        )


class DriverCreationForm(UserCreationForm):

    license_number = forms.CharField(
        required=True,
        validators=[license_validation]
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):

    license_number = forms.CharField(
        required=True,
        validators=[license_validation]
    )

    class Meta:
        model = get_user_model()
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
