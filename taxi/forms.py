from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(max_length=255)

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number", "first_name", "last_name",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError("License should be 8 characters long.")

        if not license_number[:3].isalpha() or (
                license_number[:3] != license_number[:3].upper()):
            raise ValidationError(
                "First three symbols should be uppercase letters."
            )

        if not license_number[3:].isnumeric():
            raise ValidationError("Last five symbols should be numbers.")

        return license_number


class DriverLicenseUpdateForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Driver
        exclude = ["username", ]
        fields = UserCreationForm.Meta.fields + ("license_number", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("password")

    def clean(self):
        cleaned_data = super().clean()
        license_number = cleaned_data.get("license_number")

        if len(license_number) != 8:
            raise ValidationError("License should be 8 characters long.")

        if not license_number[:3].isalpha() or (
                license_number[:3] != license_number[:3].upper()):
            raise ValidationError(
                "First three symbols should be uppercase letters."
            )

        if not license_number[3:].isnumeric():
            raise ValidationError("Last five symbols should be numbers.")


class CarCreationView(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers", )
