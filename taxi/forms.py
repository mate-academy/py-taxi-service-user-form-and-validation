from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    DRIVER_LICENSE_LEN = 8

    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != self.DRIVER_LICENSE_LEN:
            raise ValidationError("License number must contain 8 characters")

        if not (
            license_number[0:3].isalpha()
            and license_number[0:3].isupper()
        ):
            raise ValidationError("Invalid license number")

        if not "".join(license_number[3:]).isdigit():
            raise ValidationError("Invalid license number")

        return license_number


class CarForm(forms.ModelForm):
    Car = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
