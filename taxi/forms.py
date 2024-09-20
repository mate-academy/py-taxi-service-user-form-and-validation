from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import MaxLengthValidator, RegexValidator

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[
            MaxLengthValidator(
                8, message="License number must be 8 characters long"
            ),
            RegexValidator(
                regex=r"^[A-Z]{3}\d{5}$",
                message="License number must consist of 3 uppercase letters "
                        "followed by 5 digits"
            )
        ]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class DriverCreationForm(DriverLicenseUpdateForm, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = (
            UserCreationForm.Meta.fields
            + ("license_number", "first_name", "last_name", "email")
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
