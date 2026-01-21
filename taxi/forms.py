from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.forms.models import ModelForm

from taxi.models import Driver, Car


MIN_LEN = 8
CUSTOM_VALIDATOR = RegexValidator(
    regex=r"^[A-Z]{3}\d{5}$",
    message="Must be exactly 8 characters: "
            "first 3 uppercase letters, followed by 5 digits."
)


class DriverForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        min_length=MIN_LEN,
        validators=[CUSTOM_VALIDATOR, ]
    )

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number", )


class DriverLicenseUpdateForm(ModelForm):
    license_number = forms.CharField(
        required=True,
        min_length=MIN_LEN,
        validators=[CUSTOM_VALIDATOR, ]
    )

    class Meta:
        model = Driver
        fields = ["license_number", ]


class CarCreateForm(ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        required=False,
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
