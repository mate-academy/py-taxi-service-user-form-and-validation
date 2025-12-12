from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms.widgets import CheckboxSelectMultiple

from .models import Car
from django.forms import ModelForm, ModelMultipleChoiceField
import re


User = get_user_model()


class DriverLicenseUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        pattern = r"^[A-Z]{3}\d{5}$"
        if not re.match(pattern, license_number):
            raise ValidationError(
                "License must be 3 uppercase letters followed by 5 digits."
            )
        return license_number


class DriverCreateForm(UserCreationForm, DriverLicenseUpdateForm):
    class Meta:
        model = User
        fields = (
            "username",
            "license_number",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )


class CarForm(ModelForm):
    drivers = ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
