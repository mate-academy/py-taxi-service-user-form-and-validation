from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number_field(value):
    if not (len(value) == 8 and value[:3].isalpha()
            and value[:3].isupper() and value[3:].isdigit()):
        raise ValidationError(
            "Field must be 8 characters long, first 3 characters must be "
            "capital letters, last 5 characters must be numbers!"
        )


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        validators=[validate_license_number_field]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number"
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[validate_license_number_field]
    )

    class Meta:
        model = Driver
        fields = ["license_number"]


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
