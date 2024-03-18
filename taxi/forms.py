from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number(license_number):
    license_number_size = 8
    seria_size = 3
    if len(license_number) != license_number_size:
        raise ValidationError(
            f"License number must be at {license_number_size} chars"
        )
    seria = license_number[:seria_size]
    number = license_number[seria_size:]
    if not seria.isalpha() or seria != seria.upper():
        raise ValidationError(
            f"License number must start with {seria_size} uppercase letters"
        )
    if not number.isdigit():
        raise ValidationError(f"Last {len(number)} char must be digit")


class CustomDriverCreateForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        widget=forms.TextInput(),
        validators=[validate_license_number]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        widget=forms.TextInput(),
        validators=[validate_license_number]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
