from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if not license_number:
            raise ValidationError("The field cannot be empty")

        if len(license_number) != 8:
            raise ValidationError("The field must have 8 characters")

        if not (license_number[:3].isalpha() and license_number[:3].isupper()):
            raise ValidationError("The first 3 letters must be capitalized")

        if not license_number[3:].isdigit():
            raise ValidationError("The last 5 characters must be numbers")

        return license_number


class DriverCreationForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = "__all__"

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if not license_number:
            raise ValidationError("The field cannot be empty")

        if len(license_number) != 8:
            raise ValidationError("The field must have 8 characters")

        if not (license_number[:3].isalpha() and license_number[:3].isupper()):
            raise ValidationError("The first 3 letters must be capitalized")

        if not license_number[3:].isdigit():
            raise ValidationError("The last 5 characters must be numbers")

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
