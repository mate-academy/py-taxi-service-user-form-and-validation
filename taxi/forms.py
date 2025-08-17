from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import RegexValidator

from taxi.models import Car

license_validator = RegexValidator(
    regex=r"^[A-Z]{3}\d{5}$",
    message="Enter a valid license number "
            "(3 uppercase letters + 5 digits, e.g., ABC12345).",
)
help_text = (
    "License number must contain 8 "
    "characters: 3 uppercase letters "
    "followed by 5 digits (e.g., ABC12345)."
)


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        help_text=help_text,
        validators=[license_validator]
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "license_number", )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        help_text=help_text,
        validators=[license_validator]
    )

    class Meta:
        model = get_user_model()
        fields = ("license_number", )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Car
        fields = "__all__"
