from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",
                                                 "first_name",
                                                 "last_name")


def validate_license_number(license_number):
    if (
        len(license_number) != 8
        or not license_number[:3].isupper()
        or not license_number[:3].isalpha()
        or not license_number[3:].isdigit()
    ):
        raise ValidationError(
            "License must consist 8 characters, "
            "first 3 are uppercase letters and last 5 are digits"
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(required=True,
                                     validators=[validate_license_number])

    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
