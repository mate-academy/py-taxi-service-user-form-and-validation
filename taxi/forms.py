from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.views import View

from taxi.models import Driver, Car


class LicenseNumberValidatorMixin(forms.ModelForm):
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) == 8:
            RegexValidator(
                regex=r"[A-Z]{3}\d{5}",
                message="Ensure it meets the format of 3 uppercase "
                        "letters followed by 5 digits. Exemple:'ABC12345'"
            )(license_number)
            return license_number
        raise ValidationError("License length must be 8 characters")


class DriverForm(LicenseNumberValidatorMixin, UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "license_number",
        )


class DriverLicenseUpdateForm(LicenseNumberValidatorMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
