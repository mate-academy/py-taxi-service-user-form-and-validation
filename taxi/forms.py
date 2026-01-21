from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number(value):
    if (len(value) == 8
            and value[0:3].isalpha()
            and value[0:3].isupper()
            and value[3:].isnumeric()):
        return value
    raise ValidationError("Please enter a valid driver's license number.")


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[validate_license_number],
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[validate_license_number],
    )

    class Meta:
        model = Driver
        fields = ("license_number",)
