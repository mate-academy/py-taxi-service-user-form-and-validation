from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    MIN_LENGTH = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != DriverLicenseUpdateForm.MIN_LENGTH:
            raise ValidationError(
                f"License number should be min "
                f"{DriverLicenseUpdateForm.MIN_LENGTH}"
            )
        elif (not license_number[:3].isalpha()
              or license_number[:3] != license_number[:3].upper()):
            raise ValidationError(
                "First 3 characters should be Capital letters"
            )
        elif not license_number[3:].isdigit():
            raise ValidationError("Last 5 characters should be digits")
        return license_number


class DriverCreateForm(UserCreationForm, DriverLicenseUpdateForm):
    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "license_number"
        )

        def clean_licence_number(self):
            return super().clean_licence_number()


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
