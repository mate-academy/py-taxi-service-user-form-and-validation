from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.forms import ModelMultipleChoiceField
from taxi.models import Driver, Manufacturer, Car


class DriverCreationForm(UserCreationForm):

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
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

        if len(license_number) != 8:
            raise ValidationError(
                "license number must consist of 8 characters"
            )

        if not license_number[:3].isalpha():
            raise ValidationError("First 3 characters must be letter")

        if not license_number[:3].isupper():
            raise ValidationError("First 3 letters must be upper")

        if not license_number[3:].isdigit():
            raise ValidationError("Last 5 characters must be digits")

        return license_number


class CarForm(forms.ModelForm):

    drivers = ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
