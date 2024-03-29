from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_custom(value):
    if len(value) != 8:
        raise ValidationError(
            f"password's length must be 8 characters, "
            f"length you've given is {len(value)} char."
        )
    if not (value[:3].isupper() and value[:3].isalpha()):
        raise ValidationError("First 3 characters nust be uppercase letters")
    if not value[-5:].isdigit():
        raise ValidationError("Last 5 characters must be digits")


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        required=False, validators=[validate_custom]
    )

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=False, validators=[validate_custom]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
