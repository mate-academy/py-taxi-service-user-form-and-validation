from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class CarForm(forms.ModelForm):

    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


def validate_license_number(license_number: str) -> str:
    if len(license_number) != 8:
        raise forms.ValidationError("Must consist only of 8 characters")

    if (not license_number[:3].isalpha()
            or license_number[:3] != license_number[:3].upper()):
        raise forms.ValidationError(
            "First 3 characters must consist only of uppercase letters"
        )

    if not license_number[-5:].isdigit():
        raise forms.ValidationError(
            "Last 5 characters must consist only of digits"
        )

    return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        return validate_license_number(license_number)
