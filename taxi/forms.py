from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re

from .models import Car
from django import forms


class DriverLicenseUpdateForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise ValidationError("License must be 3 "
                                  "uppercase letters followed by 5 digits")

        return license_number


class CarCreate(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
