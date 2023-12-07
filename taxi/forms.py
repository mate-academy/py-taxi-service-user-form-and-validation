from django import forms
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class LicenseNumberValidationMixin(forms.ModelForm):
    LENGTH = 8
    FIRST_LETTERS = 3
    LAST_DIGITS = 5

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != self.LENGTH:
            raise forms.ValidationError(
                f"License number length should be {self.LENGTH} characters"
            )
        if not (
            license_number[: self.FIRST_LETTERS].isupper()
            and license_number[: self.FIRST_LETTERS].isalpha()
        ):
            raise forms.ValidationError(
                f"First {self.FIRST_LETTERS} letters should be uppercase"
            )
        if not license_number[self.FIRST_LETTERS:].isdigit():
            raise forms.ValidationError(
                f"Last {self.LAST_DIGITS} characters should be digits"
            )
        return license_number


class DriverCreationForm(LicenseNumberValidationMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }
