from django import forms
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must be 8 characters long"
            )
        if (
                not license_number[:3].isalpha()
                or license_number[:3].upper() != license_number[:3]
        ):
            raise forms.ValidationError(
                "First 3 characters must be letters and uppercase"
            )
        if not license_number[3:].isdigit():
            raise forms.ValidationError(
                "Last 5 characters must be numbers"
            )
        return license_number


class DriverCreationForm(UserCreationForm, DriverLicenseUpdateForm):
    cars = forms.ModelMultipleChoiceField(
        queryset=Car.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
            "email",
            "cars")

    def clean_license_numbers(self):
        return super().clean_license_number()

    def save(self, commit=True):
        driver = super().save()
        driver.cars.set(self.cleaned_data["cars"])
        if commit:
            driver.save()
        return driver
