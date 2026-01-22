from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from taxi.models import Driver, Car
from taxi.validation_patterns import (
    LICENSE_NUMBER_PATTERN,
    LICENSE_NUMBER_HELP_TEXT,
    LICENSE_NUMBER_MESSAGE,
)


class CarBaseForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"


class CarCreationForm(CarBaseForm):
    pass


class CarUpdateForm(CarBaseForm):
    pass


class DriverBaseForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        validators=[
            RegexValidator(
                LICENSE_NUMBER_PATTERN, message=LICENSE_NUMBER_MESSAGE
            ),
        ],
        help_text=LICENSE_NUMBER_HELP_TEXT,
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class DriverCreationForm(UserCreationForm, DriverBaseForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
        )


class DriverLicenseUpdateForm(DriverBaseForm):
    class Meta(DriverBaseForm.Meta):
        pass
