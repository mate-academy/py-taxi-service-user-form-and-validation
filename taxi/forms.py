from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def clean_license_number(cleaned_data):
    license_number = cleaned_data["license_number"]

    if len(license_number) != 8:
        raise ValidationError(
            "License number must consists only of 8 characters"
        )

    if (
            not license_number[:3].isupper()
            or not license_number[:3].isalpha()
    ):
        raise ValidationError(
            "First 3 characters must be uppercase letters"
        )

    if not license_number[-5:].isnumeric():
        raise ValidationError(
            "Last 5 characters must be digits"
        )

    return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )

    def clean(self):
        clean_license_number(self.cleaned_data)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean(self):
        clean_license_number(self.cleaned_data)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"


class CarAssignOrDeleteForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = []
