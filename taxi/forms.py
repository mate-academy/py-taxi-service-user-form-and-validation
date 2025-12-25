from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator

from taxi.models import Driver, Car


class LicenseNumberValidatorMixin:
    license_number = forms.CharField(
        required=True,
        validators=[MinLengthValidator(8), MaxLengthValidator(8)]
    )

    def clean_license_number(self):

        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError(
                "License number must be exactly 8 characters long."
            )

        if (
                not license_number[:3].isupper()
                or not license_number[:3].isalpha()
        ):
            raise ValidationError(
                "First 3 characters of license number "
                "must be uppercase letters"
            )

        if not license_number[3:].isdigit():
            raise ValidationError(
                "Last 5 characters of license number must be digits"
            )

        return license_number


class DriverCreationForm(UserCreationForm, LicenseNumberValidatorMixin):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm, LicenseNumberValidatorMixin):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
