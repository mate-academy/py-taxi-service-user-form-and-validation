from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


class DriverLicenseValidator:
    COUNT_LETTERS = 3
    COUNT_NUMBERS = 5
    LICENSE_NUMBER_LENGTH = COUNT_LETTERS + COUNT_NUMBERS

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not len(license_number) == self.LICENSE_NUMBER_LENGTH:
            raise ValidationError(
                f"Length license number should be {self.LICENSE_NUMBER_LENGTH}"
            )

        if (
                not license_number[:self.COUNT_LETTERS].isupper()
                or not license_number[:self.COUNT_LETTERS].isalpha()
        ):
            raise ValidationError(
                f"First {self.COUNT_LETTERS} symbols should be upper letters!"
            )

        if not license_number[self.COUNT_LETTERS:].isdigit():
            raise ValidationError(
                f"Last {self.COUNT_LETTERS} symbols should be digits!"
            )
        return license_number


class DriverCreationForm(
    DriverLicenseValidator,
    UserCreationForm
):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(DriverLicenseValidator, forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer",)
