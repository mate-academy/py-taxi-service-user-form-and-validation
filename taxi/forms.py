from django.forms import ModelForm, ValidationError, CheckboxSelectMultiple
from .models import Car, Driver


class DriverLicenseUpdateForm(ModelForm):
    LICENSE_LEN = 8
    INT_START_INDEX = 3

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError(
                f"Consist only of {DriverLicenseUpdateForm.LICENSE_LEN}"
                "characters"
            )
        if (
            not license_number[
                : DriverLicenseUpdateForm.INT_START_INDEX
            ].isupper()
            or not license_number[
                : DriverLicenseUpdateForm.INT_START_INDEX
            ].isalpha()
        ):
            raise ValidationError(
                f"First {DriverLicenseUpdateForm.INT_START_INDEX}"
                " characters are uppercase letters"
            )
        if not license_number[
            DriverLicenseUpdateForm.INT_START_INDEX :
        ].isdigit():
            must_be_letters = (
                DriverLicenseUpdateForm.LICENSE_LEN
                - DriverLicenseUpdateForm.INT_START_INDEX
            )
            raise ValidationError(
                f"First {must_be_letters} characters are uppercase letters"
            )
        return license_number


class CarCreateForm(ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {"drivers": CheckboxSelectMultiple}
