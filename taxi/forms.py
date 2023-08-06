from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
import re

from taxi.models import Driver, Car


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverLicenseUpdateForm(forms.ModelForm):

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError(
                "The license number must contain exactly 8 characters."
            )
        if not re.match(r"^[A-Z]{3}", license_number):
            raise forms.ValidationError(
                "The first 3 characters must be capital letters."
            )
        if not license_number[3:].isdigit():
            raise forms.ValidationError(
                "The last 5 characters must be numbers."
            )
        return license_number

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("license_number",)
