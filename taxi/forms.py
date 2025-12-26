from django import forms
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class LicenseValidationMixin:
    NUMBER_OF_CHARACTERS = 8
    NUMBER_FIRST_UPPERCASE = 3
    NUMBER_LAST_DIGITS = 5

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != self.NUMBER_OF_CHARACTERS:
            raise forms.ValidationError(
                f"Must consist of only {self.NUMBER_OF_CHARACTERS} characters!"
            )
        if not license_number[:self.NUMBER_FIRST_UPPERCASE].isalpha():
            raise forms.ValidationError(
                f"The first {self.NUMBER_FIRST_UPPERCASE} "
                f"characters must be letter!"
            )
        if not license_number[:self.NUMBER_FIRST_UPPERCASE].isupper():
            raise forms.ValidationError(
                f"The first {self.NUMBER_FIRST_UPPERCASE} "
                f"characters must be uppercase!"
            )
        if not license_number[-self.NUMBER_LAST_DIGITS:].isdigit():
            raise forms.ValidationError(
                f"The last {self.NUMBER_LAST_DIGITS} "
                f"characters must be numbers!"
            )

        return license_number


class DriverForm(LicenseValidationMixin, UserCreationForm):
    class Meta:
        model = Driver
        fields = (
            "username",
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(LicenseValidationMixin, forms.ModelForm):
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
        fields = "__all__"
