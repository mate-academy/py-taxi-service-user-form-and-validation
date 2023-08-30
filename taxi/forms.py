from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car
from django import forms


class DriverCreateForm(UserCreationForm):

    def clean_license_number(self):
        return DriverLicenseUpdateForm.clean_license_number(self)

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    NUM_CHAR = 8
    NUM_UPP_CHAR = 3
    NUM_DIGITS = 5

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != DriverLicenseUpdateForm.NUM_CHAR:
            raise ValidationError(
                f"Ensure that license number consist "
                f"{DriverLicenseUpdateForm.NUM_CHAR} symbols"
            )

        if not license_number[:DriverLicenseUpdateForm.NUM_UPP_CHAR].isalpha():
            raise ValidationError(
                f"First "
                f"{DriverLicenseUpdateForm.NUM_UPP_CHAR}"
                f" chars must be letters"
            )

        if not license_number[:DriverLicenseUpdateForm.NUM_UPP_CHAR].isupper():
            raise ValidationError(
                f"First "
                f"{DriverLicenseUpdateForm.NUM_UPP_CHAR} "
                f"chars must be uppercase letter"
            )

        if not license_number[-DriverLicenseUpdateForm.NUM_DIGITS:].isdigit():
            raise ValidationError(
                f"Last "
                f"{DriverLicenseUpdateForm.NUM_DIGITS}"
                f" chars must be digits"
            )

        return license_number


class DriverForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
