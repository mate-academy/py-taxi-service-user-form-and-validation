from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):

    REQUIRED_LENGTH = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != self.REQUIRED_LENGTH:
            raise ValidationError(
                f"License number may consist of only "
                f"{self.REQUIRED_LENGTH} characters!"
            )
        elif (
            not license_number[:3].isalpha()
            or license_number[:3] != license_number[:3].upper()
        ):
            raise ValidationError(
                "First 3 characters of License"
                " number should be uppercase letters"
            )
        elif not license_number[3:].isdigit():
            raise ValidationError(
                "Last 5 characters of License number should be digits"
            )
        return license_number


class DriverCreationForm(UserCreationForm, DriverLicenseUpdateForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "license_number",
        )

    def clean_license_number(self):
        return super().clean_license_number()


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
