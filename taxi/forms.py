from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from taxi.models import Car

VALIDATION_REGEX = r"^[A-Z]{3}[0-9]{5}"
VALIDATION_MESSAGE = (
    "Consist only of 8 characters\n"
    "First 3 characters are uppercase letters\n"
    "Last 5 characters are digits\n"
)


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        validators=[
            RegexValidator(VALIDATION_REGEX, VALIDATION_MESSAGE)
        ]
    )

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        validators=[
            RegexValidator(VALIDATION_REGEX, VALIDATION_MESSAGE)
        ]
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
