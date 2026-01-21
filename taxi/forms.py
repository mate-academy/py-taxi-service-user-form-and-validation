from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator

from taxi.models import Driver, Car

license_number_validator = RegexValidator(
    regex=r"^[A-Z]{3}\d{5}$",
    message="License number must consist of 8 characters: "
            + "the first 3 are uppercase letters, the last 5 are digits."
)


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(validators=[license_number_validator])

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number")


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(validators=[license_number_validator])

    class Meta:
        model = Driver
        fields = ("license_number",)
