from debug_toolbar.utils import hidden_paths
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def clean_license_number(license_number):
    char_part, num_part = license_number[:3], license_number[3:]
    errors = []

    if len(license_number) != 8:
        errors.append(
            "License number has to consist of 8 characters strictly!"
        )
    if char_part != char_part.upper() or not char_part.isalpha():
        errors.append(
            "First 3 characters of license number "
            "have to be uppercase letters!!!"
        )
    if not num_part.isnumeric():
        errors.append(
            "The last 5 characters of license number have to be digits!!!"
        )

    if errors:
        raise ValidationError(errors)
    return license_number


class DriverCreateForm(UserCreationForm):
    user_permissions = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    license_number = forms.CharField(
        validators=(clean_license_number,)
    )

    class Meta:
        model = Driver
        fields = "__all__"
        exclude = ("groups",)


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[clean_license_number]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarUpdateDriverForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = "__all__"
