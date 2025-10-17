from django import forms
from django.forms import CheckboxSelectMultiple

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["model", "manufacturer", "drivers"]
        widgets = {"drivers": CheckboxSelectMultiple}
