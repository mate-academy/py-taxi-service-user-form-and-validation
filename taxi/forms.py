from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Car, Driver


class DriverForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(str(license_number)) != 8:
            raise ValidationError("License number should consists only of 8 characters")

        first_3 = license_number[:3]
        last_5 = license_number[3:]

        if not all([letter.istitle() for letter in first_3]):
            raise ValidationError("First 3 letters should be uppercase letters")
        if not all([letter.isnumeric() for letter in last_5]):
            raise ValidationError("Last 5 characters must be digits")

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
