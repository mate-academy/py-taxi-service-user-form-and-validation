from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError("The length of the number must be 8 (eight)!")
    elif not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise ValidationError(
            "The first three characters must be uppercase letters!"
        )
    elif not license_number[-5:].isdigit():
        raise ValidationError("The last five characters must be numbers!")

    return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])
