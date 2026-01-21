from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class LicenseCleanForm(forms.ModelForm):
    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError(
                "Ensure license number is 8 characters length"
            )
        if not (license_number[:3].isalpha() and license_number[:3].isupper()):
            raise ValidationError(
                "Ensure first 3 characters are uppercase letters"
            )
        if not license_number[3:].isdigit():
            raise ValidationError(
                "Ensure last 5 characters are digits"
            )
        return license_number


class DriverCreationForm(LicenseCleanForm, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "license_number"
        )


class DriverLicenseUpdateForm(LicenseCleanForm, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
