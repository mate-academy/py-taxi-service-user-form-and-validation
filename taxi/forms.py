from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Driver, Car


def validate_license_number(license_number: str) -> None:
    if len(license_number) != 8:
        raise ValidationError(
            "License number must be 8 characters long"
        )
    if not license_number[:3].isalpha():
        raise ValidationError(
            "License number must start with letters"
        )
    if not license_number[:3].isupper():
        raise ValidationError(
            "License number must start with uppercase letters"
        )
    if not license_number[3:].isdigit():
        raise ValidationError(
            "License number must end with digits"
        )


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = "__all__"

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        try:
            validate_license_number(license_number)
            return license_number
        except ValidationError as e:
            raise ValidationError(e.message)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        try:
            validate_license_number(license_number)
            return license_number
        except ValidationError as e:
            raise ValidationError(
                e.message, code="invalid", params={"value": 302}
            )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
        widgets = {"drivers": forms.CheckboxSelectMultiple}
