from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car, Driver


class DriverLicenseValidator:
    AMOUNT_LETTERS = 3
    AMOUNT_NUMBERS = 5
    LICENSE_NUMBER_SYMBOLS_AMOUNT = AMOUNT_LETTERS + AMOUNT_NUMBERS

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not len(license_number) == self.LICENSE_NUMBER_SYMBOLS_AMOUNT:
            raise ValidationError(
                f"Length license number should be "
                f"{self.LICENSE_NUMBER_SYMBOLS_AMOUNT}"
            )

        if (
                not license_number[:self.AMOUNT_LETTERS].isupper()
                or not license_number[:self.AMOUNT_LETTERS].isalpha()
        ):
            raise ValidationError(
                f"First {self.AMOUNT_LETTERS} symbols should be "
                f"uppercase letters!"
            )

        if not license_number[self.AMOUNT_LETTERS:].isdigit():
            raise ValidationError(
                f"Last {self.AMOUNT_LETTERS} symbols should be digits!"
            )
        return license_number


class DriverCreationForm(
    DriverLicenseValidator,
    UserCreationForm
):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(DriverLicenseValidator, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer",)
