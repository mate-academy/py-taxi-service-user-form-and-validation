from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

from taxi.models import Driver, Car


license_validator = RegexValidator(
    regex=r"^[A-Z]{3}\d{5}$",
    message="Consist only of 8 characters, "
            "First 3 characters are uppercase letters, "
            "Last 5 characters are digits"
)


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        max_length=8,
        min_length=8,
        validators=[license_validator]
    )

    class Meta:
        model = Driver
        fields = ("license_number", )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
