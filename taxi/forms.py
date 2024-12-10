# import re

from django.contrib.auth.forms import UserCreationForm
# from django.core.exceptions import ValidationError
from django.forms import ModelForm, CheckboxSelectMultiple

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number"
        )

    # def clean_license_number(self):
    #     data = self.cleaned_data["license_number"]
    #
    #     if not re.fullmatch(r"^[A-Z]{3}[0-9]{5}$", data):
    #         raise ValidationError("The license number is incorrect.")
    #
    #     return data


class DriverLicenseUpdateForm(ModelForm):
    class Meta:
        model = Driver
        fields = ("first_name", "last_name", "license_number")

    # def clean_license_number(self):
    #     data = self.cleaned_data["license_number"]
    #
    #     if not re.fullmatch(r"^[A-Z]{3}[0-9]{5}$", data):
    #         raise ValidationError("The license number is incorrect.")
    #
    #     return data


class CarCreateForm(ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {"drivers": CheckboxSelectMultiple}
