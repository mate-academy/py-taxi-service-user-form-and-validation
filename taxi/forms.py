from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car, Driver


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverLicenseValidationForm(forms.ModelForm):
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not (
                license_number[:3].isalpha()
                and license_number[:3].isupper()
                and license_number[-5:].isdigit()
        ):
            raise ValidationError(
                "A driver's license must contain 8 characters. "
                "The first 3 characters are uppercase letters. "
                "The last 5 characters are digits. "
            )

        return license_number


class DriverCreationForm(DriverLicenseValidationForm, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )


class DriverLicenseUpdateForm(DriverLicenseValidationForm, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)
