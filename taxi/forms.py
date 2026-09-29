from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from taxi.models import Car


license_validator = RegexValidator(
    regex=r"^[A-Z]{3}[0-9]{5}$",
    message="Please use proper format for license number (ABC12345)",
)


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[license_validator],
    )

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "email",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[license_validator],
    )

    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {"drivers": forms.CheckboxSelectMultiple}
