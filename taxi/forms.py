from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxLengthValidator, RegexValidator

from taxi.models import Driver, Car
from django import forms


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[
            MaxLengthValidator(
                8,
                message="License number must be 8 symbols"
            ),
            RegexValidator(
                regex=r"^[A-Z]{3}\d{5}$",
                message="License number must contain 3 first "
                        "capital letter and 5 numbers next"
            )
        ]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class DriverCreationForm(UserCreationForm, DriverLicenseUpdateForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
