from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def clean_license_number(value):
    if (len(value) != 8
            or not value[:3].isalpha()
            or not value[:3].isupper()
            or not value[3:].isdigit()):
        raise ValidationError("Ensure the license number "
                              "consist only of 8 characters, "
                              "first 3 characters are uppercase letters, "
                              "last 5 characters are digits"
                              )


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        validators=[clean_license_number]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = (UserCreationForm.Meta.fields
                  + ("first_name", "last_name", "license_number", ))


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[clean_license_number]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("license_number", )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
