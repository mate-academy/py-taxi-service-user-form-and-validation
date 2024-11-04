from django import forms
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )


class DriverDeleteForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = []


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = [
            "license_number",
        ]


class CarCreationForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple()
        }
