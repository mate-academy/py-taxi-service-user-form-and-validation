from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car, Driver


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    LICENSE_LENGTH = 8
    NUMBER_OF_FIRST_UPPERCASE_LETTERS = 3
    NUMBER_OF_LAST_DIGITS = 5

    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != self.LICENSE_LENGTH:
            raise ValidationError(
                "License numbers should consist of total "
                f"{self.LICENSE_LENGTH} characters! "
                f"First {self.NUMBER_OF_FIRST_UPPERCASE_LETTERS}"
                f" are uppercase letters "
                f"and last {self.NUMBER_OF_LAST_DIGITS} are digits."
            )

        for letter in license_number[:self.NUMBER_OF_FIRST_UPPERCASE_LETTERS]:
            if letter.isdecimal() or letter.islower():
                raise ValidationError(
                    f"First {self.NUMBER_OF_FIRST_UPPERCASE_LETTERS} "
                    "characters should be uppercase letters!"
                )

        for digit in license_number[self.NUMBER_OF_FIRST_UPPERCASE_LETTERS:]:
            if not digit.isdigit():
                raise ValidationError(
                    f"Last {self.NUMBER_OF_LAST_DIGITS} "
                    "characters should be digits!"
                )

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
