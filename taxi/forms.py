from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError(
                "The lengths of license number should be equal to 8 characters"
            )
        elif not (license_number[:3].isupper()
                  and license_number[:3].isalpha()):
            raise ValidationError(
                "First 3 characters should be uppercase letters"
            )
        elif not license_number[3:].isdigit():
            raise ValidationError("Last 5 characters should be digits")

        return license_number
