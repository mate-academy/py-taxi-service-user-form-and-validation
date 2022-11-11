from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError(
                "License number must consists only of 8 characters!"
            )

        if not license_number[0:3].isupper() and \
                not license_number[0:3].isalpha():
            raise ValidationError(
                "First 3 of the license number characters "
                "must be uppercase letters!"
            )

        if not license_number[-5:].isdigit():
            raise ValidationError(
                "Last 5 characters of the license "
                "number  must be digits!"
            )

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
