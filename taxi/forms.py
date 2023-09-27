from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from .models import Driver, Car


def check_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError("License number long must be 8.")
    for value in license_number[:3]:
        if not value.isupper():
            raise ValidationError("Ensure that license is correct.")
    for value in license_number[3:]:
        if not value.isdigit():
            raise ValidationError("Ensure that license is correct.")

    return license_number


class DriverUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return check_license_number(license_number)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
