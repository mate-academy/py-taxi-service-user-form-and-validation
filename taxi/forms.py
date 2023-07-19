from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class LicenseNumberValidator:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not license_number.isalnum():
            raise ValidationError("License number must contain "
                                  "only letters and numbers!")
        if len(license_number) != 8:
            raise ValidationError("License number must be 8 symbols long!")
        if not (license_number[:3].isupper() and license_number[:3].isalpha()):
            raise ValidationError("First 3 characters of the license "
                                  "must be uppercase letters!")
        if not license_number[3:].isdigit():
            raise ValidationError("Last 5 characters must be digits!")
        return license_number


class DriverCreationForm(LicenseNumberValidator, UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name")


class DriverLicenseUpdateForm(LicenseNumberValidator, forms.ModelForm):

    class Meta:
        model = Driver
        fields = ["license_number"]


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
