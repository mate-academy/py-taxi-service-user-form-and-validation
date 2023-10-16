from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Car


class LicenseNumberValidatorMixin:
    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        error_message = "First 3 characters must be uppercase letters"

        if len(license_number) != 8:
            raise ValidationError("License length should be 8 characters")

        for el in license_number[:3]:
            if el in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                raise ValidationError(error_message)

        if license_number[:3] != license_number[:3].upper():
            raise ValidationError(error_message)

        try:
            for num in license_number[3:]:
                int(num)
        except ValueError:
            raise ValidationError("Last 5 characters must be digits")

        return license_number


class DriverCreationForm(UserCreationForm, LicenseNumberValidatorMixin):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number"
        )


class DriverLicenseUpdateForm(forms.ModelForm, LicenseNumberValidatorMixin):
    class Meta:
        model = get_user_model()
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
