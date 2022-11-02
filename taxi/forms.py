from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number"
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    LICENSE_NUMBER_LENGTH = 8

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        series = license_number[:3]
        number = license_number[3:]

        if len(license_number) != self.LICENSE_NUMBER_LENGTH:
            raise ValidationError(
                "License number should contain "
                f"{self.LICENSE_NUMBER_LENGTH} characters"
            )

        if not series.isalpha() or not series.isupper():
            raise ValidationError(
                "First 3 characters should contain only letters in uppercase"
            )

        if not number.isnumeric():
            raise ValidationError(
                "Last 5 characters should contain only numeric values"
            )

        return license_number
