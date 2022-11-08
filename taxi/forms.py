from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def licence_validation(license_num):
    licence_num_len = 8
    # decided to to all-in-one check so a user will see all the requirements in
    # case of any validation error
    if (
            len(license_num) != licence_num_len
            or not (license_num[:3].isupper() and license_num[:3].isalpha())
            or not license_num[4:].isdigit()
    ):
        raise ValidationError(
            f"Licence number length must contain {licence_num_len} "
            f"symbols.\n"
            f"First 3 symbols must be letters in uppercase.\n"
            f"Rest of the symbols must be numeric."
            "  (for instance: AAA11111)"
        )


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number"
        )

    def clean_license_number(self):
        license_num = self.cleaned_data["license_number"]
        licence_validation(license_num)

        return license_num


class DriverLicenceUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_num = self.cleaned_data["license_number"]
        licence_validation(license_num)

        return license_num


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
