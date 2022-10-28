from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    LICENSE_NUMBER_LENGTH = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    @staticmethod
    def check_last_digits(license_num):

        return True

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if (
            len(license_number)
            != DriverLicenseUpdateForm.LICENSE_NUMBER_LENGTH
        ):
            raise ValidationError("License number must contain 8 characters!")

        if (
            not license_number[:3].isalpha()
            or not license_number[:3].isupper()
        ):
            raise ValidationError(
                "First 3 characters must be uppercase letters!"
            )

        if not license_number[3:].isdigit():
            raise ValidationError("Last 5 characters must be digits!")
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
