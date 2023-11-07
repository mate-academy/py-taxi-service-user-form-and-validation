from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def license_number_func(license_number):
    if (
            len(license_number) != 8
            or not license_number[0:3].isupper()
            or not license_number[-5:].isdigit()
    ):
        raise ValidationError(
            "Consist only of 8 characters, "
            "First 3 characters are uppercase letters, "
            "Last 5 characters are digits"
        )
    return license_number


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return license_number_func(license_number)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("first_name", "last_name", "license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return license_number_func(license_number)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
