from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


def valid_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError("Must be consist only of 8 characters")
    elif not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise ValidationError("First 3 characters must be uppercase letters.")
    elif not license_number[-5:].isdigit():
        raise ValidationError("Last 5 characters must be digits.")


class DriverLicenseUpdateForm(forms.ModelForm):
    min_length = 8
    license_number = forms.CharField(
        required=True,
        validators=[valid_license_number]
    )

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
        fields = "__all__"
