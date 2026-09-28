from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    LICENSE_LEN = 8
    LICENSE_LEN_LETTERS_UPPER = 3
    LICENSE_LEN_DIGITS = LICENSE_LEN - LICENSE_LEN_LETTERS_UPPER

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != self.LICENSE_LEN:
            raise forms.ValidationError(
                f"Ensure that chars count "
                f"{DriverLicenseUpdateForm.LICENSE_LEN}"
            )

        letters_part = license_number[
            : DriverLicenseUpdateForm.LICENSE_LEN_LETTERS_UPPER
        ]
        digits_part = license_number[
            DriverLicenseUpdateForm.LICENSE_LEN_LETTERS_UPPER :
        ]

        if not (letters_part.isupper() and letters_part.isalpha()):
            raise forms.ValidationError(
                f"Ensure that first "
                f"{DriverLicenseUpdateForm.LICENSE_LEN_LETTERS_UPPER} "
                f"chars must be upper chars"
            )
        if not digits_part.isdigit():
            raise forms.ValidationError(
                f"Ensure that last "
                f"{DriverLicenseUpdateForm.LICENSE_LEN_DIGITS} "
                f"chars must be digits"
            )

        return license_number


class DriverCreationForm(UserCreationForm, DriverLicenseUpdateForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
