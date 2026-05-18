from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import CheckboxSelectMultiple, ModelForm

from .models import Car


def validate_license_number(license_number):
    if (
            len(license_number) != 8
            or not license_number[:3].isupper()
            or not license_number[:3].isalpha()
            or not license_number[3:].isdigit()
    ):
        raise ValidationError(
            "License number must contain 3 uppercase letters "
            "followed by 5 digits."
        )


class DriverLicenseUpdateForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "license_number",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": CheckboxSelectMultiple(),
        }
