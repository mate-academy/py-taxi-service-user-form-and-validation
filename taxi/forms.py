from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car
from django import forms


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name"
        )


class DriverUpdateLicenseForm(forms.ModelForm):
    LEN_LICENSE_NUMBER = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if license_number != DriverUpdateLicenseForm.LEN_LICENSE_NUMBER:
            raise ValidationError(
                f"Amount symbols must be"
                f"{DriverUpdateLicenseForm.LEN_LICENSE_NUMBER}"
            )

        if (
                not license_number[:3].isupper()
                and not license_number[:3].isalpha()
        ):
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
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
