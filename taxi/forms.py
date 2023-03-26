from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    DRIVER_LICENSE_LENGTH = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != DriverLicenseUpdateForm.\
                DRIVER_LICENSE_LENGTH:
            raise ValidationError(
                "The license number must be "
                f"{DriverLicenseUpdateForm.DRIVER_LICENSE_LENGTH}"
                " characters long."
            )
        for word in license_number[:3]:
            if not word.isupper():
                raise ValidationError(
                    "First three characters must be capital letters"
                )
        for num in license_number[3:]:
            if not num.isdigit():
                raise ValidationError(
                    "Last 5 characters must be numbers"
                )
        return license_number


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
