from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import MinLengthValidator, RegexValidator

from taxi.models import Driver, Car

LICENSE_NUMBER_REGEX = r"^[A-Z]{3}\d{5}$"
LICENSE_NUMBER_ERROR_MESSAGE = ("License must be 3 uppercase letters "
                                "followed by 5 digits (e.g., ABC12345).")

license_number_field = forms.CharField(
    required=True,
    validators=[
        RegexValidator(
            regex=LICENSE_NUMBER_REGEX,
            message=LICENSE_NUMBER_ERROR_MESSAGE,
        )
    ],
)


class DriverCreationForm(UserCreationForm):
    license_number = license_number_field

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = (UserCreationForm.Meta.fields
                  + ("license_number", "first_name", "last_name", ))


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = license_number_field

    class Meta:
        model = Driver
        fields = ("license_number", )


class CarCreatingForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
