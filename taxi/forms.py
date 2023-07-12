from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    LICENSE_NUMBER_LENGTH = 8
    UPPERCASE_LETTERS_LENGTH = 3
    DIGITS_LENGTH = 5

    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if not license_number:
            raise forms.ValidationError("License number is required.")

        if len(license_number) != self.LICENSE_NUMBER_LENGTH:
            raise forms.ValidationError(
                f"License number must be {self.LICENSE_NUMBER_LENGTH} "
                f"characters long."
            )

        if not license_number[:self.UPPERCASE_LETTERS_LENGTH].isalpha() or (
                not license_number[:self.UPPERCASE_LETTERS_LENGTH].isupper()
        ):
            raise forms.ValidationError(
                f"First {self.UPPERCASE_LETTERS_LENGTH} characters must be "
                f"uppercase letters."
            )

        if not license_number[self.UPPERCASE_LETTERS_LENGTH:].isdigit():
            raise forms.ValidationError(
                f"Last {self.DIGITS_LENGTH} characters must be digits."
            )

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Select drivers for this car"
    )

    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "model": forms.TextInput(attrs={"placeholder": "Enter car model"}),
        }

    def clean_model(self):
        model = self.cleaned_data.get("model")
        if not model:
            raise ValidationError("Model name is required")
        return model
