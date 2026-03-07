from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator

from taxi.models import Driver, Car

license_validator = RegexValidator(
    regex=r"^[A-Z]{3}[0-9]{5}$",
)


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = ("username", "password1", "password2", "license_number")


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Car
        fields = "__all__"


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=9,
        validators=[license_validator]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)
