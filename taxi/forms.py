from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    LICENCE_LEN = 8

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if len(license_number) != 8:
            raise ValidationError(
                f"The license number must be "
                f"{self.LICENCE_LEN} characters long."
            )
        if not license_number[:4].isupper():
            raise ValidationError(
                "The license number must start with 3 UPPER CASE LETTERS"
            )
        if not license_number[4:].isdigit():
            raise ValidationError("The license number must end with 5 NUMBERS")
        return license_number


class DriverLicenseUpdateForm(UserChangeForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
