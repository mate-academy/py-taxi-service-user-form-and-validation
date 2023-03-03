from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError(
                "Ensure, that you input 8 symbols"
            )

        if not license_number[:3].isupper() or not\
                license_number[:3].isalpha():
            raise ValidationError(
                "Ensure, that first 3 symbols are uppercase letters"
            )

        if not license_number[3:].isdigit():
            raise ValidationError(
                "Ensure, that symbols from 4 to 8 are digits"
            )

        return license_number


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True,
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
