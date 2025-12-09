import re
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from taxi.models import Driver, Car


class LicenseNumberValidationMixin(forms.ModelForm):
    def clean_license_number(self):
        value = self.cleaned_data["license_number"]
        if not re.match(r"^[A-Z]{3}\d{5}$", value):
            raise ValidationError(
                "The license number must"
                "consist of 3 uppercase letters and 5 digits"
            )
        return value


class DriverCreationForm(LicenseNumberValidationMixin, UserCreationForm):
    license_number = forms.CharField(
        required=True,
        help_text="The license number must consist"
                  "of 3 uppercase letters and 5 digits")

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = (
            "license_number",
        )


class CarForm(forms.ModelForm):
    driver = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "driver",)
