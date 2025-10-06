from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number(value):
    if len(value) != 8:
        raise ValidationError("The license number must consist of exactly 8 characters.")
    if not (value[:3].isalpha()) or not (value[:3].isupper()):
        raise ValidationError("The first 3 characters must be uppercase letters.")
    if not (value[3:].isdigit()):
        raise ValidationError("The last 5 characters must be digits.")


class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(validators=[validate_license_number])

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverUpdateLicenseForm(forms.ModelForm):
    license_number = forms.CharField(validators=[validate_license_number])

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = ["model", "manufacturer", "drivers"]
