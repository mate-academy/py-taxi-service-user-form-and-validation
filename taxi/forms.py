from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        User = get_user_model()
        model = User
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return check_licence_number(license_number)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        User = get_user_model()
        model = User
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return check_licence_number(license_number)


def check_licence_number(license_number):
    len_license_number = 8
    first_alpha_character = 3
    last_numeric_character = 5

    if len(license_number) != len_license_number:
        raise ValidationError(
            f"Length of license_number must be equal to {len_license_number}"
        )
    if not license_number[0:3].isalpha():
        raise ValidationError(
            f"First {first_alpha_character} characters must be alphabetical"
        )
    if license_number[0:3].upper() != license_number[0:3]:
        raise ValidationError(
            "Alphabetical characters must be in uppercase"
        )
    if not license_number[3:len_license_number].isdigit():
        raise ValidationError(
            f"Last {last_numeric_character} characters must be numeric"
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
