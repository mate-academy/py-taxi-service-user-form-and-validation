from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number(self):
    license_number = self.cleaned_data["license_number"]

    if len(license_number) != 8:
        raise ValidationError("License number should be 8 characters long")

    if not license_number[:3].isalpha():
        raise ValidationError(
            "License number should start with 3 uppercase letters"
        )

    if not license_number[3:].isnumeric():
        raise ValidationError("5 last characters should be digits")

    return license_number


class DriverCreationForm(UserCreationForm):
    def clean_license_number(self):
        return validate_license_number(self)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    def clean_license_number(self):
        return validate_license_number(self)

    class Meta:
        model = get_user_model()
        fields = ["license_number", ]


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
