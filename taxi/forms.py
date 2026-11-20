from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Car, Driver


class DriverCreationForm(UserCreationForm):
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError("License number must be exactly 8 characters long")

        letters = license_number[:3]
        digits = license_number[3:]

        if not letters.isalpha() or not letters.isupper():
            raise ValidationError("First 3 characters must be uppercase letters")
        if not digits.isdigit():
            raise ValidationError("Last 5 characters must be digits")

        return license_number

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError("License number must be exactly 8 characters long")

        letters = license_number[:3]
        digits = license_number[3:]

        if not letters.isalpha() or not letters.isupper():
            raise ValidationError("First 3 characters must be uppercase letters")
        if not digits.isdigit():
            raise ValidationError("Last 5 characters must be digits")

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
