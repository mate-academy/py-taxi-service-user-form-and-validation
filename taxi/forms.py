import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Car  # explicit import is clearer and flake8-friendly

UserModel = get_user_model()


def validate_license_number(value):
    """Validate license format: 3 uppercase letters + 5 digits."""
    if not re.match(r"^[A-Z]{3}\d{5}$", value):
        raise ValidationError(
            "O número da licença deve ter 3 letras maiúsculas seguidas "
            "por 5 dígitos (ex: ABC12345)."
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[validate_license_number],
        help_text="Formato: ABC12345 (3 letras maiúsculas + 5 dígitos)",
    )

    class Meta:
        model = UserModel
        fields = ["license_number"]


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[validate_license_number],
        help_text="Formato: ABC12345 (3 letras maiúsculas + 5 dígitos)",
    )

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = UserCreationForm.Meta.fields + ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=UserModel.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
