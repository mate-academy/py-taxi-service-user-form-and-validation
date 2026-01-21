from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from taxi.models import Driver, Car


class DriverCreateForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = [
            "username",
            "first_name",
            "last_name",
            "license_number",
        ]


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{3}\d{5}$",
                message="Number of license must consist "
                        "only of 8 characters, first 3 characters "
                        "are uppercase letters, "
                        "last 5 characters are digits."
            ),
        ]
    )

    class Meta:
        model = Driver
        fields = [
            "license_number",
        ]


class CarListForm(forms.Form):
    cars = forms.ModelMultipleChoiceField(
        queryset=Car.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    driver = forms.ModelChoiceField(
        queryset=Driver.objects.all(),
        required=True,
        label="Select a driver"
    )
