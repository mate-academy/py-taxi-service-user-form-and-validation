from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


def validate_license_number(license_number: str) -> str:
    if len(license_number) != 8:
        raise ValidationError(
            "Your driver's license number must contain "
            "8 characters. "
            "For example: ABC12345"
        )
    letters_validate = not license_number[:3].isalpha()
    case_validate = not license_number[:3].isupper()
    digits_validate = not license_number[3:].isdigit()
    if letters_validate or case_validate or digits_validate:
        raise ValidationError(
            "Your driver's license number must contain "
            "3 capital letters and 5 digits. "
            "For example: ABC12345"
        )
    return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
