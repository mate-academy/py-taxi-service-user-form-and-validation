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
            "email",
            "license_number"
        )

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError(
                "Ensure that length license_number is 8"
            )

        elif (not license_number[:3].isalpha()
              or not license_number[:3].isupper()):
            raise ValidationError("Ensure that first 3 letters "
                                  "in license_number are in uppercase")

        elif not license_number[3:].isdigit():
            raise ValidationError("Ensure that after 3 letters "
                                  "in license_number are only digits")
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
        )

    def clean_license_number(self):
        return DriverCreationForm.clean_license_number(self)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
