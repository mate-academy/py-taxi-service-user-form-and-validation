from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.core.validators import RegexValidator

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    REGEX = r"^[A-Z]{3}\d{5}$"

    license_number = forms.CharField(
        required=True,
        validators=[
            RegexValidator(
                regex=REGEX,
                message="The appropriate format is 'AAA00000'",
            ),
        ],
    )

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    REGEX = r"^[A-Z]{3}\d{5}$"

    license_number = forms.CharField(
        required=True,
        validators=[
            RegexValidator(
                regex=REGEX,
                message="The appropriate format is 'AAA00000'",
            ),
        ],
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
