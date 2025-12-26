from django import forms
from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class LicenseNumberMixin():
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError(
                "License number length must be equal to 8."
            )

        if not (license_number[:3].isalpha() and license_number[:3].isupper()):
            raise ValidationError(
                "First 3 letters must be in upper case."
            )

        if not license_number[3:].isnumeric():
            raise ValidationError(
                "Last 5 characters must be numbers."
            )
        return license_number


class DriverCreationForm(LicenseNumberMixin, UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "license_number",
        )


class DriverLicenseUpdateForm(LicenseNumberMixin, forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
