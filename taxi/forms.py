from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.safestring import mark_safe

from taxi.models import Driver, Car

LICENSE_HELP_TEXT = mark_safe(
    "<ul>"
    "<li>Your license number should only consist of 8 characters long.</li>"
    "<li>Your license number's first 3 characters are uppercase letters.</li>"
    "<li>Your license number's last 5 characters are digits.</li>"
    "</ul>"
)


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError(
            "Ensure that license number consist of exactly 8 characters."
        )

    if not (license_number[:3].isupper() and license_number[:3].isalpha()):
        raise ValidationError(
            "Ensure that first 3 characters are uppercase letters."
        )

    if not license_number[-5:].isdigit():
        raise ValidationError(
            "Ensure that last 5 characters are digits."
        )

    return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )
        help_texts = {
            "license_number": LICENSE_HELP_TEXT,
        }

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )
        help_texts = {
            "license_number": LICENSE_HELP_TEXT,
        }

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class CarCreationForm(ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Car
        fields = "__all__"
