import django
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name",
                                                 "last_name",
                                                 "license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    TOTAL_LENGTH = 8
    START_UPP_LET = 3
    NUM_END_DIGITS = 5

    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != self.TOTAL_LENGTH:
            raise ValidationError(
                f"Ensure that length is {self.TOTAL_LENGTH} characters")

        if not license_number[3:].isdigit():
            raise ValidationError(
                f"Ensure that last {self.NUM_END_DIGITS} are digits")

        if not (license_number[:self.START_UPP_LET].isupper()
                and license_number[:self.START_UPP_LET].isalpha()):
            raise ValidationError(
                "Ensure that first "
                f"{self.START_UPP_LET} are uppercase letters"
            )

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
