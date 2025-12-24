from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField()

    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError("Driver license should have 8 symbols")
        if not (license_number[:3].isalpha() and license_number[:3].isupper()):
            raise ValidationError(
                "First 3 characters must be uppercase letters"
            )
        if not license_number[-5:].isdigit():
            raise ValidationError(
                "Driver license last 5 symbols should be digits"
            )

        return license_number


class DriverLicenseCreateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number", )

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError("Driver license should have 8 symbols")
        if not (license_number[:3].isalpha() and license_number[:3].isupper()):
            raise ValidationError(
                "First 3 characters must be uppercase letters"
            )
        if not license_number[-5:].isdigit():
            raise ValidationError(
                "Driver license last 5 symbols should be digits"
            )

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
