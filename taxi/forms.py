from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class LicenseNumberValidationMixin(forms.ModelForm):

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError(
                "Number should be exactly 8 characters long!"
            )
        prefix = license_number[:3]
        if not (prefix.isalpha() and prefix.isupper()):
            raise ValidationError(
                "First three characters should be uppercase letters (A-Z)!"
            )
        numbers = license_number[3:]
        if not (numbers.isdigit()):
            raise ValidationError("Last 5 charachters should be digits (0-9)!")
        return license_number


class DriverCreationForm(LicenseNumberValidationMixin, UserCreationForm):

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
