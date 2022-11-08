from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
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

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        uppercase_letters = license_number[:3]
        digits = license_number[3:]

        if len(license_number) != 8:
            raise ValidationError(
                "Licence number must consist of 8 characters"
            )

        if (
                not uppercase_letters.isalpha()
                or uppercase_letters != uppercase_letters.upper()
        ):
            raise ValidationError(
                "First 3 characters must be uppercase letters"
            )

        if not digits.isdigit():
            raise ValidationError("Last 5 characters must be digits")

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
