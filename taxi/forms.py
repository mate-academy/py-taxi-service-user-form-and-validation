from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from .models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "last_name",
            "first_name",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[
            RegexValidator(
                regex=r"[A-Z]{3}\d{5}",
                message="Enter 3 letters and 5 numbers. "
                "For example 'ABC12345'",
            )
        ]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
