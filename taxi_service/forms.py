from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator

from taxi.models import Driver, Car


class LicenseNumberValidatorMixin:
    license_number = forms.CharField(
        required=True,
        validators=[MinLengthValidator(8), MaxLengthValidator(8)]
    )
