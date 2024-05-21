from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from .models import Driver, Car


class LicenseNumberValidatorMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if len(license_number) != 8:
            raise ValidationError(
                "The license number must be exactly 8 characters long."
            )
        if (not license_number[:3].isupper()
                or not license_number[:3].isalpha()):
            raise ValidationError(
                "The first three characters of the license number "
                "must be uppercase letters."
            )
        if not license_number[3:].isdigit():
            raise ValidationError(
                "The last five characters of the license number "
                "must be digits."
            )
        return license_number


class DriverCreateForm(LicenseNumberValidatorMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "license_number",
        )


class DriverLicenseUpdateForm(LicenseNumberValidatorMixin, UserChangeForm):
    password = None

    class Meta(UserChangeForm.Meta):
        model = Driver
        fields = ("first_name", "last_name", "email", "license_number")


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
