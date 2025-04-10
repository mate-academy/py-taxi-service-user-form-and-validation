from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    LICENSE_NUMBER_LENGTH = 8

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name",
                                                 "last_name",
                                                 "license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != self.LICENSE_NUMBER_LENGTH:
            raise forms.ValidationError(f"Invalid license number. "
                                        f"Ensure that license number "
                                        f"is {self.LICENSE_NUMBER_LENGTH} "
                                        f"symbols.")

        three_symbols = license_number[:3]

        if not three_symbols.isalpha():
            error_message = "Please ensure that first 3 characters are letters"
            raise forms.ValidationError(f"{error_message}")

        if three_symbols.upper() != three_symbols:
            error_message = ("Please ensure that first "
                             "3 characters are uppercase letters")
            raise forms.ValidationError(f"{error_message}")

        last_5_symbols = license_number[3:]
        if not last_5_symbols.isdigit():
            err_message = "Please ensure that last 5 characters are digits"
            raise forms.ValidationError(f"{err_message}")

        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    LICENSE_NUMBER_LENGTH = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):

        license_number = self.cleaned_data["license_number"]
        if len(license_number) != self.LICENSE_NUMBER_LENGTH:
            raise forms.ValidationError(f"Invalid license number. "
                                        f"Ensure that license number "
                                        f"is {self.LICENSE_NUMBER_LENGTH} "
                                        f"symbols.")

        three_symbols = license_number[:3]

        if not three_symbols.isalpha():
            err_message = "Please ensure that first 3 characters are letters"
            raise forms.ValidationError(f"{err_message}")

        if three_symbols.upper() != three_symbols:
            message = ("Please ensure that first 3 characters "
                       "are uppercase letters")
            raise forms.ValidationError(f"{message}")

        last_5_symbols = license_number[3:]
        if not last_5_symbols.isdigit():
            message = "Please ensure that last 5 characters are digits"
            raise forms.ValidationError(f" {message}")

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    class Meta:
        model = Car
        fields = "__all__"
