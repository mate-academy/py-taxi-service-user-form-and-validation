from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import RegexValidator
from django.forms import CheckboxSelectMultiple

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        validators=[
            RegexValidator(r"^[A-Z]{3}\d{5}$"),
        ],
    )

    class Meta(UserCreationForm):
        model = Driver
        fields = (
            "username",
            "first_name",
            "last_name",
            "license_number",
            "password1",
            "password2",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[
            RegexValidator(r"^[A-Z]{3}\d{5}$"),
        ],
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
