from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator

from taxi.models import Driver, Car

license_number_validator = RegexValidator(
    regex=r"^[A-Z]{3}\d{5}$",
    message="License number must contain 3 uppercase letters "
            "followed by 5 digits (e.g., ABC12345)"
)


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        validators=[license_number_validator]
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        validators=[license_number_validator]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
