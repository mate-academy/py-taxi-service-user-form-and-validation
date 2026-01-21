from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.models import Driver, Car


def validate_license_number(license_number):
    if (len(license_number) == 8
            and license_number[:3].isalpha()
            and license_number[:3].isupper()
            and license_number[3:].isdigit()):
        return license_number
    raise forms.ValidationError("Invalid license number")


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        validators=[validate_license_number]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        validators=[validate_license_number]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
