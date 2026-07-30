from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


def validate_license_number(license_number: str) -> None:
    if len(license_number) != 8:
        raise ValidationError("Ensure license number must have only 8 symbols")

    if (
        license_number[:3].upper() != license_number[:3]
        or not license_number[:3].isalpha()
    ):
        raise ValidationError(
            "Ensure first three symbols "
            "of license number are letters and uppercase"
        )

    if not license_number[3:].isdigit():
        raise ValidationError("Ensure last five symbols are digits")


class DriverLicenseCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = (UserCreationForm.Meta.fields
                  + ("license_number", "first_name", "last_name", ))

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        validate_license_number(license_number)
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
