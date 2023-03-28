from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    CHARACTERS_NUMBER = 8

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != DriverLicenseUpdateForm.CHARACTERS_NUMBER:
            raise ValidationError(
                f"Ensure that the license number consist only of "
                f"{DriverLicenseUpdateForm.CHARACTERS_NUMBER} characters"
            )

        if not (license_number[:3].isalpha() and license_number[:3].isupper()):
            raise ValidationError(
                "Ensure that the first 3 characters are uppercase letters"
            )

        if not license_number[3:].isdigit():
            raise ValidationError(
                "Ensure that the last 5 characters are numbers"
            )

        return license_number


class DriverCreationForm(UserCreationForm, DriverLicenseUpdateForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "email", "license_number",
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
