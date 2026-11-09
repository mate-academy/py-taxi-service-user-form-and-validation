from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import RegexValidator

from .models import Driver, Car


license_number_validator = RegexValidator(
    regex=r"^[A-Z]{3}\d{5}$",
    message="License_number "
            "must contain 3 uppercase letters and 5 digits.",
)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        validators=[license_number_validator],
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(UserChangeForm):
    password = None
    password2 = None
    license_number = forms.CharField(
        required=True,
        validators=[license_number_validator],
    )

    class Meta(UserChangeForm.Meta):
        model = Driver
        fields = (
            "license_number",
        )
