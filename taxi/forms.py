from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from .models import Car

LICENSE_REGEX = RegexValidator(
    regex=r"^[A-Z]{3}\d{5}$",
    message="License number must have 3 uppercase letters "
            "followed by 5 digits."
)

User = get_user_model()


class DriverForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        min_length=8,
        validators=[LICENSE_REGEX]
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "license_number"]


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        min_length=8,
        validators=[LICENSE_REGEX]
    )

    class Meta:
        model = User
        fields = ["license_number"]


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
