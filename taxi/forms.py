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
            "license_number",
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverLicenseUpdateForm(forms.ModelForm):
    LENGTH = 8
    SEPARATION_INDEX = 3

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        letters_part =\
            license_number[:DriverLicenseUpdateForm.SEPARATION_INDEX]
        numbers_part =\
            license_number[DriverLicenseUpdateForm.SEPARATION_INDEX:]
        if len(license_number) != DriverLicenseUpdateForm.LENGTH:
            raise ValidationError(
                "Ensure that value is "
                f"{DriverLicenseUpdateForm.LENGTH} characters long"
            )
        if not letters_part.isalpha() or letters_part != letters_part.upper():
            raise ValidationError(
                "Ensure that first 3 characters are uppercase letters"
            )
        if not numbers_part.isnumeric():
            raise ValidationError(
                "Ensure that last 5 characters are numbers"
            )
        return license_number
