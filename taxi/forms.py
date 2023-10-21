from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


from taxi.models import Driver, Car


class LicenseNumberValidator:
    LICENSE_LENGTH = 8
    UPPER_COUNT = 3

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != self.LICENSE_LENGTH:
            raise ValidationError(
                "License number should consist of 8 characters"
            )
        elif not (
                license_number[:self.UPPER_COUNT].isupper()
        ) or not (
                license_number[:self.UPPER_COUNT].isalpha()
        ):
            raise ValidationError(
                "First 3 characters should be uppercase letters"
            )
        elif not license_number[self.UPPER_COUNT:].isdigit():
            raise ValidationError("Last 5 characters should be digits")

        return license_number


class DriverCreationForm(UserCreationForm, LicenseNumberValidator):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )


class DriverLicenseUpdateForm(forms.ModelForm, LicenseNumberValidator):
    class Meta:
        model = get_user_model()
        fields = ("license_number", )


class CarCreationForm(forms.ModelForm):
    driver = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "driver", )
