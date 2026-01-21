from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class LicenseNumberCleanMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError(
                "Ensure that value length is equal 8"
            )
        if not (license_number[:3].isalpha() and license_number[:3].isupper()):
            raise ValidationError(
                "Ensure that the first 3 chars are alphas and are uppers"
            )
        if not license_number[3:8].isdigit():
            raise ValidationError(
                "Ensure that the last 5 chars are digits"
            )
        return license_number


class DriverCreationForm(UserCreationForm, LicenseNumberCleanMixin):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm, LicenseNumberCleanMixin):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
