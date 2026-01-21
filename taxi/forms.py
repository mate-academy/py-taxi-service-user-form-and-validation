import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import (
    ModelForm,
    ModelMultipleChoiceField,
    CheckboxSelectMultiple,
)
from django.contrib.auth.forms import UserCreationForm

from .models import Car

pat = re.compile(r"^[A-Z]{3}[0-9]{5}$")


class CarForm(ModelForm):
    drivers = ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(), widget=CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if pat.fullmatch(license_number):
            return license_number

        raise ValidationError(
            "The format should be: 3 uppercase letters + 5 digits"
        )


class DriverLicenseUpdateForm(ModelForm):

    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if pat.fullmatch(license_number):
            return license_number

        raise ValidationError(
            "The format should be: 3 uppercase letters + 5 digits"
        )
