from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "username",
            "first_name",
            "last_name",
            "license_number"
        )


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) > 8:
            raise ValidationError(
                "Length of license number is maximum 8 characters"
            )

        if not license_number[:3].isupper():
            raise ValidationError(
                "The first three letters needs to be uppercase"
            )

        if not license_number[:3].isalpha():
            raise ValidationError(
                "The first three characters must be a letters"
            )

        if not license_number[-5:].isdigit():
            raise ValidationError(
                "The last five characters needs to be a numbers"
            )

        return license_number


class CarCreateForm(forms.ModelForm):

    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
