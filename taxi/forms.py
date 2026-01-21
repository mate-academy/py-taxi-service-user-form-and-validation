from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        label="Driver License Number",
        validators=[
            RegexValidator(
                r"^[A-Z]{3}\d{5}$",
                message="Driver license number must consist of 8 "
                        "characters: 3 uppercase letters followed by 5 digits."
            )
        ]
    )

    class Meta:
        model = Driver
        fields = ("license_number", )


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
