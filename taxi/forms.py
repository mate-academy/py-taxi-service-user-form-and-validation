from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def driver_license_validation(license_number: str) -> str:
    if len(license_number) != 8:
        raise ValidationError(
            "The licence must have 8 characters long"
        )
    elif (not license_number[:3].isalpha()
          or not license_number[:3].isupper()):
        raise ValidationError(
            "The licence number must start whit 3 uppercase letters"
        )
    elif not license_number[3:].isdigit():
        raise ValidationError(
            "Last 5 characters must be digits"
        )

    return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number", ]

    def clean_license_number(self):
        return driver_license_validation(self.cleaned_data["license_number"])


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Driver
        fields = (UserCreationForm.Meta.fields
                  + ("first_name", "last_name", "license_number", ))

    def clean_license_number(self):
        return driver_license_validation(self.cleaned_data["license_number"])


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
