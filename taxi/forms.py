from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from taxi.models import Driver, Car

license_number_validator = RegexValidator(
    regex=r"^[A-Z]{3}[0-9]{5}$",
    message=(
        "License number must consist of 8 characters: "
        "3 uppercase letters followed by 5 digits."
    ),
)


class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        validators=[license_number_validator]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        validators=[license_number_validator]
    )

    class Meta:
        model = Driver
        fields = (
            "license_number",
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
