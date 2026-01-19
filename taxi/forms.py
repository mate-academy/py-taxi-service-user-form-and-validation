from django import forms
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


def clean_license_number(license_number: str) -> str:
    if (
        len(license_number) != 8
        or not license_number[:3].isupper()
        or not license_number[3:].isdigit()
    ):
        raise forms.ValidationError("License number is invalid")
    return license_number


class DriverCreateForm(UserCreationForm):

    license_number = forms.CharField(
        required=True,
        label="License Number",
        validators=[clean_license_number],
    )

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class LicenseUpdateForm(forms.ModelForm):

    license_number = forms.CharField(
        required=True,
        label="License Number",
        validators=[clean_license_number],
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label="Drivers",
    )

    class Meta:
        model = Car
        fields = "__all__"
