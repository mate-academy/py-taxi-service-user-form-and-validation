from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from taxi.models import Driver, Car


validate_license_number = RegexValidator(
    regex=r"^[A-Z]{3}\d{5}$",
    message="The license number must consist of 3 capital letters"
            " followed by 5 numbers."
)


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = (
            "username",
            "first_name",
            "last_name",
            "license_number",
            "password1",
            "password2"
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(validators=[validate_license_number])

    class Meta:
        model = Driver
        fields = ("license_number", )


class CarCreationForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")

    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Add Drivers"
    )
