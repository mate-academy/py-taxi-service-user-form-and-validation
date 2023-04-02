from django import forms
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from .models import Driver, Car


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        return validate_license_number(self)


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        return validate_license_number(self)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


def validate_license_number(request):
    license_number = request.cleaned_data["license_number"]
    first_three = license_number[:3]
    last_five = license_number[3:]

    if len(license_number) != 8:
        raise ValidationError(
            "Ensure that license consists of 8 characters"
        )
    elif not first_three.isupper() or not first_three.isalpha():
        raise ValidationError(
            "Ensure that first three characters are uppercase letters"
        )

    elif not last_five.isdigit():
        raise ValidationError(
            "Ensure that last five characters are digits"
        )

    return license_number
