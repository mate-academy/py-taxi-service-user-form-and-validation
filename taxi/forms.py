from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms
from taxi.models import Car, Driver


def license_validator(license_number) -> str:
    if len(license_number) != 8:
        raise ValidationError(
            "The length of licence number should be 8!"
        )

    first_part = license_number[:3]
    last_part = license_number[3:]

    if not (first_part.isalpha() and first_part.isupper()):
        raise ValidationError(
            "First 3 characters should be uppercase!"
        )
    if not last_part.isdigit():
        raise ValidationError(
            "Last 5 characters should be digits!"
        )

    return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "email",
            "license_number"
        )

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data.get("license_number")
        return license_validator(license_number)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return license_validator(license_number)
