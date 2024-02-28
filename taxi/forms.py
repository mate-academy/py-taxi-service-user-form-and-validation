from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Driver, Car


class DriverCreationForm(forms.ModelForm):
    LENGTH_OF_LICENSE = 8

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != DriverCreationForm.LENGTH_OF_LICENSE:
            raise ValidationError(
                f"License number must be {DriverCreationForm.LENGTH_OF_LICENSE}"
                f" characters length."
            )
        if (
            not license_number[:3].isupper()
            or not license_number[:3].isalpha()
        ):
            raise ValidationError(
                "First 3 characters must be uppercase letters."
            )
        if not license_number[-5:].isdigit():
            raise ValidationError("Last 5 characters must be digits.")
        return license_number


class DriverLicenseUpdateForm(UserChangeForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "license_number")


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
