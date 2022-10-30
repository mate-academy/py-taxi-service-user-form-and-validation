from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "last_name",
            "first_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    LETTERS = 3
    DIGITS = 5
    TOTAL_QUANTITY = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        first_letters = license_number[0:DriverLicenseUpdateForm.LETTERS]

        if len(license_number) != DriverLicenseUpdateForm.TOTAL_QUANTITY:
            raise ValidationError(
                "Ensure that value has "
                f"{DriverLicenseUpdateForm.TOTAL_QUANTITY} characters"
            )

        if not (first_letters.isalpha() and first_letters.isupper()):
            raise ValidationError(
                f"Ensure that first {DriverLicenseUpdateForm.LETTERS} "
                "characters are uppercase"
            )

        if not license_number[DriverLicenseUpdateForm.LETTERS:].isdigit():
            raise ValidationError(
                f"Ensure that last {DriverLicenseUpdateForm.DIGITS} "
                "characters are digits"
            )

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
