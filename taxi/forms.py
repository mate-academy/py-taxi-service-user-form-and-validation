from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "email", "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    LICENSE_LEN = 8

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != DriverLicenseUpdateForm.LICENSE_LEN:
            raise ValidationError(
                ("License number consist only of "
                 f"{DriverLicenseUpdateForm.LICENSE_LEN} characters")
            )

        if len([True for char in license_number[:3] if char.isupper()]) != 3:
            raise ValidationError(
                "First 3 characters must be uppercase letters"
            )

        if not license_number[3:].isdigit():
            raise ValidationError(
                "Last 5 characters must be digits"
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
