from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def clean_license_number(license_number: str) -> str:
    if not (
            len(license_number) == 8
            and license_number[:3].isalpha()
            and license_number[:3].isupper()
            and license_number[3:].isdigit()
    ):
        raise ValidationError(
            "license_number does not consist only of 8 characters, "
            "or first 3 characters are not uppercase letters, "
            "or last 5 characters are not digits"
        )
    return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        validators=[clean_license_number]
    )

    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        validators=[clean_license_number]
    )

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
