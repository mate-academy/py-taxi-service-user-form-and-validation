from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Driver, Car

from django import forms
from django.contrib.auth.forms import UserCreationForm


class DriverCreationForm(UserCreationForm, forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "license_number"
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError(
                "Invalid license number, must be 8 characters long"
            )
        if (not license_number[0:3].isalpha()
                or license_number[0:3] != license_number[0:3].upper()):
            raise ValidationError(
                "Invalid license number, first 3 characters "
                "must be uppercase letters"
            )
        if not license_number[3:].isdigit():
            raise ValidationError(
                "Invalid license number, last 5 characters must be digits"
            )
        return license_number


class DriverLicenseUpdateForm(DriverCreationForm):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
