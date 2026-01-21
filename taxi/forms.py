from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from taxi.models import Driver, Car


license_validator = RegexValidator(
    regex=r"^[A-Z]{3}\d{5}$",
    message=("Value must contain of 3 uppercase letters "
             "and 5 digits")
)


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[license_validator]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number", )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[license_validator]
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
