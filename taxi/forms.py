from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Driver, Car


class LicenseNumberMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError(
                "License number must be 8 characters long"
            )

        if not license_number[:3].isupper():
            raise ValidationError(
                "First 3 characters must be uppercase letters"
            )

        if not license_number[:3].isalpha():
            raise ValidationError(
                "First 2 characters must be uppercase letters"
            )

        if not license_number[3:].isdigit():
            raise ValidationError(
                "Last 5 characters must be digits"
            )

        return license_number


class CarUpdateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreateForm(LicenseNumberMixin, UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "username",
            "email",
            "first_name",
            "last_name"
        )


class DriverLicenseUpdateForm(LicenseNumberMixin, UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Driver
        fields = ["license_number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("password", None)
