from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not license_number[:3].isalpha() or not license_number[:3].isupper():
            raise ValidationError("The first 3 characters must be CAPITAL LETTERS!")
        elif not license_number[3:].isdigit():
            raise ValidationError("The last 5 characters must be NUMBERS!")

        return license_number

    class Meta:
        model = Driver
        fields = ("username", "first_name", "last_name", "license_number",)


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
