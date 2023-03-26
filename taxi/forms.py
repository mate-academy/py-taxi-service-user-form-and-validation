from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    LENGTH_LICENSE_NUMBER = 8

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    LENGTH_LICENSE_NUMBER = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != DriverCreationForm.LENGTH_LICENSE_NUMBER:
            raise ValidationError(
                f"License number consist only "
                f"{DriverCreationForm.LENGTH_LICENSE_NUMBER}"
            )
        for char in license_number[:3]:
            if char != char.upper() or not char.isalpha():
                raise ValidationError(
                    "First 3 characters are uppercase letters"
                )

        for char in license_number[3:]:
            if not char.isdigit():
                raise ValidationError(
                    "Last 5 characters are digits"
                )

        return license_number


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    manufacturer = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
