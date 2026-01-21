from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class DriverForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{3}\d{5}$",
                message="For license number use 3 uppercase and 5 digits.",
            )
        ]
    )

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number"
        )


class DriverLicenseUpdateForm(DriverForm):
    class Meta:
        model = DriverForm.Meta.model
        fields = ["license_number"]


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
